import os

def llm_match_score(job_desc, resume_text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # No API key: return a dummy score for development
        return 50.0

    import openai
    openai.api_key = api_key
    prompt = f"""
    Given the following job description and resume, rate how well the resume matches the job on a scale of 0 to 100.
    Job Description: {job_desc}
    Resume: {resume_text}
    Score:
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10,
        temperature=0
    )
    score_str = response.choices[0].text.strip().split()[0]
    try:
        score = float(score_str)
    except ValueError:
        score = 0.0
    return score 