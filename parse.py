from langchain_core.prompts import ChatPromptTemplate
import cohere

cohere_api_key = "gdtBTLAUe0w1tRM8FWdLHQ46l5TErYu8MYOkrNnc"
cohere_client = cohere.Client(cohere_api_key)

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string (''). "
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_cohere(dom_chunks, parse_description):
    parsed_results = []

    try:
        for i, chunk in enumerate(dom_chunks, start=1):
            prompt = template.format(
                dom_content=chunk,
                parse_description=parse_description
            )

            response = cohere_client.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=300,
                temperature=0.5
            )

            output = response.generations[0].text.strip()
            print(f"[🔍] Parsed Chunk {i}/{len(dom_chunks)}")
            parsed_results.append(output)

        return "\n".join(parsed_results)

    except Exception as e:
        print(f"[❌] Error parsing content: {e}")
        return "Parsing failed due to an error."
