from crewai import Task

def create_resume_tailoring_task(agent, job_description, base_resume):
    return Task(
        description=(
            f"IMPORTANT: You must use the EXACT personal information (name, contact details, education, experience) from the base resume below. Do not change the person's name or invent new information.\n\n"
            f"BASE RESUME:\n{base_resume}\n\n"
            f"JOB DESCRIPTION:\n{job_description}\n\n"
            f"TASKS:\n"
            f"1. Analyze the job description above to identify key skills, experiences, and keywords.\n"
            f"2. Tailor the base resume by highlighting the candidate's actual experiences and skills that are most relevant to the job.\n"
            f"3. Incorporate the identified keywords naturally into the tailored resume.\n"
            f"4. Generate a compelling cover letter using the candidate's real name and background.\n\n"
            f"CRITICAL RULES:\n"
            f"- Use the EXACT name from the base resume\n"
            f"- Use ONLY experiences and qualifications that exist in the base resume\n"
            f"- Do not fabricate or exaggerate any information\n"
            f"- Keep all personal details (name, contact info) exactly as provided"
        ),
        expected_output=(
            "A JSON object with two keys: 'tailored_resume' and 'cover_letter'. "
            "The value for each key should be a string containing the respective document."
        ),
        agent=agent
    )