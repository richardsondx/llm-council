import asyncio
from unittest.mock import MagicMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.council import stage1_collect_responses, stage3_synthesize_final
from backend.config import COUNCIL_MODELS, COUNCIL_ROLES, CHAIRMAN_ROLE

async def verify_roles():
    print("Verifying Council Roles...")
    
    # Mock query_model to inspect arguments
    with patch('backend.openrouter.query_model') as mock_query:
        mock_query.return_value = {'content': 'Mock response', 'reasoning_details': None}
        
        # Test Stage 1
        print("\n--- Testing Stage 1 ---")
        results = await stage1_collect_responses("Test query")
        
        # Check calls for Stage 1
        # We expect len(COUNCIL_MODELS) calls
        # We need to verify that each call had the correct system message
        
        # Get all calls to query_model
        # Note: query_models_parallel calls query_model
        
        # Since query_models_parallel uses asyncio.gather, the order of calls might vary,
        # but we can check if each model received its role.
        
        call_args_list = mock_query.call_args_list
        
        # We expect 4 calls for stage 1 (based on default config)
        print(f"Stage 1 calls: {len(call_args_list)}")
        
        for i, call in enumerate(call_args_list):
            args, kwargs = call
            model = args[0]
            messages = args[1]
            
            print(f"Call {i+1}: Model={model}")
            for msg in messages:
                print(f"  Role: {msg['role']}, Content: {msg['content'][:50]}...")
                
            # Verify role injection
            if messages[0]['role'] == 'system':
                print(f"  [PASS] System role found: {messages[0]['content']}")
            else:
                print(f"  [FAIL] No system role found for {model}")

        # Verify return structure
        print("\n--- Verifying Return Structure ---")
        for res in results:
            if 'role' in res and res['role']:
                print(f"  [PASS] Role found in response for {res['model']}: {res['role']}")
            else:
                print(f"  [FAIL] No role found in response for {res['model']}")

        # Reset mock for Stage 3
        mock_query.reset_mock()
        
        # Test Stage 3
        print("\n--- Testing Stage 3 ---")
        
        # We need to patch query_model in backend.council because it's imported there
        with patch('backend.council.query_model') as mock_query_council:
            mock_query_council.return_value = {'content': 'Mock response', 'reasoning_details': None}
            
            await stage3_synthesize_final("Test query", [], [])
            
            # Check calls for Stage 3
            call_args_list = mock_query_council.call_args_list
            print(f"Stage 3 calls: {len(call_args_list)}")
            
            if len(call_args_list) > 0:
                args, kwargs = call_args_list[0]
                messages = args[1]
                print(f"Chairman Messages:")
                for msg in messages:
                    print(f"  Role: {msg['role']}, Content: {msg['content'][:50]}...")
                
                if messages[0]['role'] == 'system' and CHAIRMAN_ROLE in messages[0]['content']:
                     print(f"  [PASS] Chairman role found: {messages[0]['content']}")
                else:
                     print(f"  [FAIL] Chairman role not found or incorrect")
            else:
                print("[FAIL] Stage 3 query_model not called")

if __name__ == "__main__":
    asyncio.run(verify_roles())
