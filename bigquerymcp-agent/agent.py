from vertexai.preview import reasoning_engines

# Define your Agent class as discussed in the PoC
class MyGovernedAgent:
    def query(self, prompt: str):
        return f"Processing {prompt}..."

# Create the engine with the gateway configuration
remote_agent = reasoning_engines.ReasoningEngine.create(
    MyGovernedAgent(),
    display_name="governed-agent-engine",
    # Pass the gateway ID in the deployment spec
    config={
        "deployment_spec": {
            "agent_gateway_config": {
                "agent_to_anywhere_config": {
                    "agent_gateway": "projects/YOUR_PROJECT/locations/us-central1/agentGateways/YOUR_GATEWAY"
                }
            }
        }
    }
)
