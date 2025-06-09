import base64
import pdfplumber
import re
import io

def encode_image(image_path):
    # Utility function to encode the image for delivery to LLM in base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text_from_pdf(file):
    """Extract text from PDF file using pdfplumber"""
    try:
        # Reset file pointer
        file.seek(0)

        text_content = ""
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"

        return text_content.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def convert_report_to_markdown(text):
    """Convert medical report text to markdown format"""
    try:
        # Clean up the text
        text = text.strip()

        # Split into lines and process
        lines = text.split('\n')
        markdown_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                markdown_lines.append('')
                continue

            # Main section headers (CLINICAL HISTORY, FINDINGS, IMPRESSION, etc.)
            if re.match(r'^[A-Z\s]+:', line) and len(line.split(':')[0]) < 30:
                section_name = line.split(':')[0].strip()
                content = ':'.join(line.split(':')[1:]).strip()
                markdown_lines.append(f"## {section_name}")
                if content:
                    markdown_lines.append(content)
                markdown_lines.append('')

            # Numbered items (1., 2., 3., etc.)
            elif re.match(r'^\d+\.', line):
                markdown_lines.append(f"**{line}**")
                markdown_lines.append('')

            # Sub-items or bullet points
            elif line.startswith('-') or line.startswith('•'):
                markdown_lines.append(f"- {line[1:].strip()}")

            # Regular content
            else:
                # Check if it's a continuation of previous content
                if markdown_lines and not markdown_lines[-1].startswith('#') and markdown_lines[-1]:
                    markdown_lines.append(line)
                else:
                    markdown_lines.append(line)

        # Join and clean up
        markdown_text = '\n'.join(markdown_lines)

        # Clean up multiple empty lines
        markdown_text = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_text)

        return markdown_text.strip()

    except Exception as e:
        print(f"Error converting to markdown: {e}")
        return text  # Return original text if conversion fails
