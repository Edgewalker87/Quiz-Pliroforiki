import json
import re

def parse_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split questions by number pattern (e.g. "1." at start of line)
    raw_questions = re.split(r'\n(?=\d+\.)', content.strip())
    
    for raw_q in raw_questions:
        lines = raw_q.strip().split('\n')
        if not lines:
            continue

        # First line is the question number and text, e.g. "1. Η ελευθερία ..."
        question_line = lines[0]
        question_text = re.sub(r'^\d+\.\s*', '', question_line).strip()

        options = []
        correct_found = False

        # Process answer lines (usually lines starting with α., β., γ., δ.)
        for opt_line in lines[1:]:
            # Extract option letter and text
            m = re.match(r'([α-δ])\.\s*(.*)', opt_line)
            if not m:
                continue
            letter = m.group(1)
            answer_text = m.group(2).strip()

            # Check if answer ends with '*'
            if answer_text.endswith('*'):
                answer_text = answer_text[:-1].strip()
                correct = True
                correct_found = True
            else:
                correct = False
            
            options.append({
                "text": answer_text,
                "correct": correct
            })
        
        if not correct_found:
            print(f"Warning: No correct answer found for question: {question_text}")

        questions.append({
            "question": question_text,
            "options": options
        })
    return questions

if __name__ == "__main__":
    input_file = "questionsPDF.txt"  # <-- Your text file name here
    output_file = "questions.json"

    questions_data = parse_questions(input_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions_data, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(questions_data)} questions to {output_file}")
