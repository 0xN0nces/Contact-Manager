# 📇 Contact Manager

A simple command-line contact management system to help you organize your contacts efficiently.

## ✨ Features

- 👤 Add and manage contacts with name, email, phone, and notes
- 🔍 Search contacts by any field
- 📋 List all contacts in a organized format
- ✏️ Edit contact information
- 🗑️ Delete contacts
- 📤 Export contacts to JSON or CSV
- ✅ Email and phone number validation
- 💾 Store contacts locally in JSON format

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/contact-manager.git
cd contact-manager
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `add`: Add a new contact
- `list`: List contacts
- `view`: View contact details
- `edit`: Edit a contact
- `delete`: Delete a contact
- `export`: Export contacts to a file

## 📋 Command Options

### Add a contact:
```bash
python main.py add <name> [options]
```

Options:

- `-e, --email`: Email address
- `-p, --phone`: Phone number
- `-n, --notes`: Additional notes

### List contacts:
```bash
python main.py list [options]
```

Options:

- `-s, --search`: Search in contacts

### View a contact:
```bash
python main.py view <id>
```

### Edit a contact:
```bash
python main.py edit <id> [options]
```

Options:

- `-n, --name`: New name
- `-e, --email`: New email
- `-p, --phone`: New phone
- `--notes`: New notes

### Delete a contact:
```bash
python main.py delete <id>
```

### Export contacts:
```bash
python main.py export <output_file> [options]
```

Options:

- `-f, --format`: Export format (json, csv)

### Global options:

- `-f, --file`: Contacts file (default: ~/.contacts.json)

## 📝 Examples

### Add a contact:
```bash
# Add a basic contact
python main.py add "John Doe"
```

```bash
# Add a contact with all details
python main.py add "Jane Smith" -e "jane@example.com" -p "+1-555-123-4567" -n "Met at conference"
```

### List contacts:
```bash
# List all contacts
python main.py list
```

```bash
# Search contacts
python main.py list -s "john"
python main.py list -s "example.com"
python main.py list -s "555"
```


