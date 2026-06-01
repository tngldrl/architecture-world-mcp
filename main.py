import sys
import json
import os
from scanner import scan_code_chunks, scan_metadata
from analyzer import extract_skeleton, extract_partial_graph, synthesize_architecture
from generator import generate_avatar

def run_phase1_pipeline(gcp_project_id: str, repo_paths: list[str], output_dir: str = "output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("="*50)
    print("PHASE 1: SCANNING METADATA & EXTRACTING SKELETON")
    print("="*50)
    metadata_context = scan_metadata(repo_paths)
    print(f"Loaded {len(metadata_context)} characters of metadata context from {len(repo_paths)} repositories.\n")
    
    try:
        skeleton_json = extract_skeleton(metadata_context, gcp_project_id)
        print("Successfully extracted ecosystem skeleton.\n")
    except Exception as e:
        print(f"Failed to extract skeleton: {e}")
        return

    print("="*50)
    print("PHASE 2: SEMANTIC CHUNKING & LOCAL GRAPH EXTRACTION")
    print("="*50)
    
    code_chunks = scan_code_chunks(repo_paths)
    print(f"Divided codebase into {len(code_chunks)} semantic chunk(s).\n")
    
    partial_graphs = []
    for i, chunk_context in enumerate(code_chunks):
        print(f"Analyzing Chunk {i+1}/{len(code_chunks)}...")
        print(f"  Loaded {len(chunk_context)} characters of code context.")
        
        try:
            partial_graph = extract_partial_graph(chunk_context, skeleton_json, gcp_project_id)
            partial_graphs.append(partial_graph)
            print(f"  Successfully analyzed Chunk {i+1}.")
        except Exception as e:
            print(f"  Failed to analyze Chunk {i+1}: {e}")
            continue

    if not partial_graphs:
        print("No chunks were successfully analyzed. Exiting.")
        return

    print("\n" + "="*50)
    print("PHASE 3: SYNTHESIZING FINAL ARCHITECTURE")
    print("="*50)
    try:
        final_architecture_json = synthesize_architecture(partial_graphs, gcp_project_id)
        data = json.loads(final_architecture_json)
        
        # Save the raw JSON
        json_path = os.path.join(output_dir, "architecture.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved synthesized architecture JSON to {json_path}\n")
    except Exception as e:
        print(f"Failed to synthesize architecture: {e}")
        return
        
    print("="*50)
    print("PHASE 4: GENERATING AVATARS (IMAGEN)")
    print("="*50)
    
    microservices = data.get("microservices", [])
    if not microservices:
        print("No microservices found in the extracted JSON.")
        return
        
    for ms in microservices:
        name = ms.get("name", "unknown")
        prompt = ms.get("avatar_prompt", "")
        
        if not prompt:
            print(f"Skipping {name}: No avatar prompt generated.")
            continue
            
        print(f"\n[{name}]")
        print(f"Role: {ms.get('role_type')}")
        print(f"Scale: {ms.get('scale_and_complexity')}")
        print(f"Prompt: {prompt}")
        
        # Sanitize filename
        safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_").lower()
        image_path = os.path.join(output_dir, f"{safe_name}.png")
        
        generate_avatar(prompt, image_path, gcp_project_id)

    print("\n" + "="*50)
    print("PIPELINE COMPLETE")
    print("="*50)
    print(f"Check the '{output_dir}' directory for results.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    gcp_project_id = os.getenv("GCP_PROJECT_ID")
    if not gcp_project_id:
        print("Error: GCP_PROJECT_ID not found in environment or .env file.")
        print("Please set it in your .env file like: GCP_PROJECT_ID=your-project-id")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_repository1> [path_to_repository2 ...]")
        sys.exit(1)
        
    repo_paths = sys.argv[1:]
    run_phase1_pipeline(gcp_project_id, repo_paths)
