from flask import Flask, request, jsonify
from crewai import Crew, Process
from agents.resume_agent import resume_tailoring_agent
from agents.outreach_agent import outreach_agent
from tasks.resume_tasks import create_resume_tailoring_task
from tasks.outreach_tasks import create_outreach_task
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/process-application', methods=['POST'])
def process_application():
    data = request.json
    base_resume = data.get('resume')
    job_description = data.get('job_description')
    company_name = data.get('company_name')
    role = data.get('role')

    # Debug logging to verify data is received
    print(f"\n=== RECEIVED DATA ===")
    print(f"Company: {company_name}")
    print(f"Role: {role}")
    print(f"Resume length: {len(base_resume) if base_resume else 0}")
    print(f"Job description length: {len(job_description) if job_description else 0}")
    print(f"===================\n")

    if not all([base_resume, job_description, company_name, role]):
        return jsonify({"error": "Missing required fields"}), 400

    # Create tasks for the agents
    resume_task = create_resume_tailoring_task(resume_tailoring_agent, job_description, base_resume)
    outreach_task = create_outreach_task(outreach_agent, company_name, role, base_resume)
    
    # Create a crew with the agents and tasks
    job_application_crew = Crew(
        agents=[resume_tailoring_agent, outreach_agent],
        tasks=[resume_task, outreach_task],
        process=Process.sequential,
        verbose=True
    )

    # Kick off the crew's work
    crew_output = job_application_crew.kickoff()

    # Extract the raw output from CrewOutput object
    try:
        # Structure the response properly
        response = {
            "tailored_resume": None,
            "cover_letter": None,
            "outreach": []
        }
        
        # Extract resume and cover letter from the first task output
        if len(crew_output.tasks_output) > 0:
            resume_output = crew_output.tasks_output[0].raw
            
            # Clean JSON markdown fences if present
            resume_output = resume_output.strip()
            if resume_output.startswith('```json'):
                resume_output = resume_output[7:]  # Remove ```json
            if resume_output.startswith('```'):
                resume_output = resume_output[3:]  # Remove ```
            if resume_output.endswith('```'):
                resume_output = resume_output[:-3]  # Remove trailing ```
            resume_output = resume_output.strip()
            
            try:
                resume_data = json.loads(resume_output)
                response["tailored_resume"] = resume_data.get("tailored_resume", "")
                response["cover_letter"] = resume_data.get("cover_letter", "")
            except json.JSONDecodeError as e:
                print(f"Error parsing resume JSON: {e}")
                response["tailored_resume"] = resume_output
        
        # Extract outreach contacts from the second task output
        if len(crew_output.tasks_output) > 1:
            outreach_output = crew_output.tasks_output[1].raw
    
    # Clean JSON markdown fences if present
            outreach_output = outreach_output.strip()
            if outreach_output.startswith('```json'):
                outreach_output = outreach_output[7:]
            if outreach_output.startswith('```'):
                outreach_output = outreach_output[3:]
            if outreach_output.endswith('```'):
                outreach_output = outreach_output[:-3]
            outreach_output = outreach_output.strip()
    
    # NEW: Extract just the JSON array from the text
    # Find the first '[' and last ']'
            start_idx = outreach_output.find('[')
            end_idx = outreach_output.rfind(']')
    
            if start_idx != -1 and end_idx != -1:
                outreach_output = outreach_output[start_idx:end_idx + 1]
    
            try:
                outreach_data = json.loads(outreach_output)
                if isinstance(outreach_data, list):
                    response["outreach"] = outreach_data
                else:
                    response["outreach"] = [outreach_data]
            except json.JSONDecodeError as e:
                print(f"Error parsing outreach JSON: {e}")
                print(f"Failed to parse: {outreach_output[:500]}")
                response["outreach"] = []
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing crew output: {e}")
        return jsonify({"error": f"Failed to process crew output: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)