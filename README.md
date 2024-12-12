# JustProcess: Automated Envelope Processing System

JustProcess is a Python-based automation tool designed to streamline the processing of scanned physical envelopes by integrating Optical Character Recognition (OCR) and web automation. This tool reduces manual labor, increases efficiency, and offers significant cost savings.

## Features

- **OCR Integration**: Utilizes Tesseract to extract reference numbers from scanned images.
- **Dynamic Web Automation**: Uses Selenium for automated dashboard interactions, including entering reference numbers and uploading files.
- **HEIC to JPG Conversion**: Converts iPhone's HEIC images to JPG for compatibility with OCR processing.
- **Error Handling and Retry Mechanism**: Ensures robustness by handling errors during file processing and retries for seamless operation.
- **Multi-threading**: Keeps the dashboard active in a separate thread, ensuring uninterrupted operation.

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/charmanc/justprocess.git
   cd justprocess
   \`\`\`

2. Install the required dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract) and configure the \`pytesseract\` path in the script.

## Usage

1. Place the files to be processed in the \`uploads\` directory.
2. Run the script:
   \`\`\`bash
   python justprocess.py
   \`\`\`

3. The tool will automatically extract reference numbers, enter them into the dashboard, and upload the files.

## Code Structure

- **\`keep_running_webpage\`**: Ensures the dashboard is always active in a separate thread.
- **\`heic_to_jpg\`**: Converts HEIC images to JPG format.
- **\`find_refnum\`**: Extracts reference numbers using OCR.
- **\`refnum_entry\`**: Automates entering reference numbers into the dashboard.
- **\`upload_file\`**: Handles file uploads through the dashboard.
- **Error Handling**: Implements retries and corrective actions for common issues like OCR misreads.

## Performance

- **Efficiency**: Reduces manual processing time by 63%, from 2 minutes to 45 seconds per envelope.
- **Cost Savings**: Decreases processing cost per envelope by 50%, saving up to €6,750 monthly.
- **Throughput**: Processes 70–80 envelopes per hour, compared to 30–40 manually.

## Future Enhancements

- Integrate barcode recognition using Pyzbar.
- Train Tesseract for better OCR accuracy with user-specific datasets.
- Add support for industrial scanners for faster image processing.

## Acknowledgements

Special thanks to the Justsnap GmbH team for providing the opportunity to develop and test this tool in a real-world use case.
