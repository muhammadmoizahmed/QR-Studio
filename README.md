# QR Studio - Professional QR Code Generator

A modern, full-featured QR Code Generator built with Python and Flask. Features real-time preview, multiple QR types, extensive customization, and a beautiful UI.

![QR Studio](static/images/qr-studio-banner.svg)

## Features

### QR Types Supported
- Website URL
- Plain Text
- Email with subject & body
- Phone Number
- WiFi Network
- vCard (Contact)
- WhatsApp Message

### Customization Options
- Custom QR code colors (fill & background)
- Real-time color preview
- Adjustable size (box size)
- Error correction levels (Low, Medium, High, Quartile)
- Logo overlay support
- Multiple download formats (PNG, SVG)

### Modern UI Features
- Dark/Light mode toggle
- Drag & drop file upload
- Toast notifications
- Loading spinners
- Responsive design (mobile-friendly)
- Real-time QR preview
- History persistence (localStorage)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qr-studio.git
   cd qr-studio
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## Usage

### Basic QR Generation
1. Select QR type from dropdown
2. Enter required data (URL, text, email, etc.)
3. Customize colors if needed
4. Click "Generate QR Code"
5. Download your QR code

### With Logo
1. Upload a logo image (PNG/JPG recommended)
2. The logo will be centered on the QR code
3. Generate and download

### Real-time Preview
- Colors update instantly as you change them
- Preview generates automatically when you have data entered
- 300ms debounce to prevent excessive API calls

## API Endpoints

### Generate QR (Full)
```
POST /api/generate
Content-Type: multipart/form-data

Parameters:
- qr_type: url|text|email|phone|wifi|vcard|whatsapp
- url, text, email, etc. (based on qr_type)
- fill_color: hex color (default: #000000)
- back_color: hex color (default: #FFFFFF)
- box_size: integer (default: 25)
- error_correction: L|M|Q|H
- logo_file: optional image file
```

### Quick Preview
```
POST /api/preview
Content-Type: multipart/form-data

Parameters:
- Same as /api/generate but optimized for speed
- Returns smaller, faster QR for preview
```

### Download QR
```
GET /download/<path:filename>
Returns the QR code file as attachment
```

## Project Structure

```
qr-studio/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── .env.example          # Environment variables template
├── config.py             # Configuration settings
├── qr.py                 # QR generation logic
├── static/
│   ├── generated/        # Generated QR codes
│   ├── css/              # Stylesheets (optional)
│   └── js/               # JavaScript files (optional)
├── templates/
│   └── index.html        # Main UI template
└── uploads/              # Uploaded logo files
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

## Development

### Running in Debug Mode
```bash
python app.py
```

### Production Deployment
Use a production WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

**QR code not generating**
- Check that all required fields are filled
- Ensure logo file is valid image format
- Verify color values are valid hex codes

**Page refreshes on generate**
- Clear browser cache (Ctrl+F5)
- Check browser console for JavaScript errors

**Colors not applying**
- Colors must be valid hex codes (e.g., #FF0000)
- High contrast colors work best for QR scanning

## License

MIT License - feel free to use for personal or commercial projects.

## Support

For issues or feature requests, please open an issue on GitHub.

---

Develop Muhammad Moiz Ahmed by using Python, Flask, and Tailwind CSS
