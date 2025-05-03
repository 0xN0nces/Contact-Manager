#!/usr/bin/env python3

import argparse
import json
import os
import re
from datetime import datetime

# Constants
DEFAULT_CONTACTS_FILE = os.path.expanduser("~/.contacts.json")

def load_contacts(file_path=DEFAULT_CONTACTS_FILE):
    """Load contacts from file"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {file_path} is corrupted")
            return []
    return []

def save_contacts(contacts, file_path=DEFAULT_CONTACTS_FILE):
    """Save contacts to file"""
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w') as f:
            json.dump(contacts, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving contacts: {e}")
        return False

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number format"""
    # Remove any non-digit characters
    cleaned = re.sub(r'[^0-9]', '', phone)
    # Check if it's between 10-15 digits
    return 10 <= len(cleaned) <= 15

def add_contact(name, email=None, phone=None, notes=None, file_path=DEFAULT_CONTACTS_FILE):
    """Add a new contact"""
    contacts = load_contacts(file_path)
    
    # Validate inputs
    if email and not validate_email(email):
        print(f"Invalid email format: {email}")
        return False
    
    if phone and not validate_phone(phone):
        print(f"Invalid phone format: {phone}")
        return False
    
    # Create contact ID
    contact_id = 1
    if contacts:
        contact_id = max(contact["id"] for contact in contacts) + 1
    
    # Create contact
    contact = {
        "id": contact_id,
        "name": name,
        "email": email,
        "phone": phone,
        "notes": notes,
        "created": datetime.now().isoformat(),
        "modified": datetime.now().isoformat()
    }
    
    contacts.append(contact)
    
    if save_contacts(contacts, file_path):
        print(f"Contact added: #{contact_id} - {name}")
        return True
    return False

def list_contacts(search_term=None, file_path=DEFAULT_CONTACTS_FILE):
    """List all contacts with optional search"""
    contacts = load_contacts(file_path)
    
    if not contacts:
        print("No contacts found")
        return
    
    # Filter contacts if search term provided
    if search_term:
        search_term = search_term.lower()
        filtered_contacts = []
        for contact in contacts:
            # Search in name, email, phone, and notes
            search_fields = [
                str(contact.get("name", "")),
                str(contact.get("email", "")),
                str(contact.get("phone", "")),
                str(contact.get("notes", ""))
            ]
            if any(search_term in field.lower() for field in search_fields):
                filtered_contacts.append(contact)
        contacts = filtered_contacts
    
    if not contacts:
        print(f"No contacts found matching '{search_term}'")
        return
    
    # Sort contacts by name
    contacts.sort(key=lambda x: x["name"].lower())
    
    # Display contacts
    print("\nContacts:")
    print("=" * 70)
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Phone':<15}")
    print("-" * 70)
    
    for contact in contacts:
        email = contact.get("email", "")
        phone = contact.get("phone", "")
        print(f"{contact['id']:<5} {contact['name']:<25} {email:<30} {phone:<15}")
    
    print("=" * 70)
    print(f"Total: {len(contacts)} contacts")

def view_contact(contact_id, file_path=DEFAULT_CONTACTS_FILE):
    """View detailed information about a contact"""
    contacts = load_contacts(file_path)
    
    # Find contact
    for contact in contacts:
        if contact["id"] == contact_id:
            print("\nContact Details:")
            print("=" * 40)
            print(f"ID: #{contact['id']}")
            print(f"Name: {contact['name']}")
            print(f"Email: {contact.get('email', 'N/A')}")
            print(f"Phone: {contact.get('phone', 'N/A')}")
            if contact.get('notes'):
                print(f"Notes: {contact['notes']}")
            print(f"Created: {contact['created']}")
            print(f"Modified: {contact['modified']}")
            print("=" * 40)
            return True
    
    print(f"Contact #{contact_id} not found")
    return False

def edit_contact(contact_id, name=None, email=None, phone=None, notes=None, file_path=DEFAULT_CONTACTS_FILE):
    """Edit an existing contact"""
    contacts = load_contacts(file_path)
    
    # Find contact
    for contact in contacts:
        if contact["id"] == contact_id:
            # Update fields if provided
            if name is not None:
                contact["name"] = name
            
            if email is not None:
                if email and not validate_email(email):
                    print(f"Invalid email format: {email}")
                    return False
                contact["email"] = email
            
            if phone is not None:
                if phone and not validate_phone(phone):
                    print(f"Invalid phone format: {phone}")
                    return False
                contact["phone"] = phone
            
            if notes is not None:
                contact["notes"] = notes
            
            # Update modification time
            contact["modified"] = datetime.now().isoformat()
            
            if save_contacts(contacts, file_path):
                print(f"Contact #{contact_id} updated")
                return True
            return False
    
    print(f"Contact #{contact_id} not found")
    return False

def delete_contact(contact_id, file_path=DEFAULT_CONTACTS_FILE):
    """Delete a contact"""
    contacts = load_contacts(file_path)
    
    # Find and remove contact
    for i, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            del contacts[i]
            if save_contacts(contacts, file_path):
                print(f"Contact #{contact_id} deleted")
                return True
            return False
    
    print(f"Contact #{contact_id} not found")
    return False

def export_contacts(output_file, format="json", file_path=DEFAULT_CONTACTS_FILE):
    """Export contacts to a file"""
    contacts = load_contacts(file_path)
    
    if not contacts:
        print("No contacts to export")
        return False
    
    try:
        if format.lower() == "json":
            with open(output_file, 'w') as f:
                json.dump(contacts, f, indent=2)
            print(f"Contacts exported to {output_file} in JSON format")
            return True
        
        elif format.lower() == "csv":
            import csv
            
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["ID", "Name", "Email", "Phone", "Notes", "Created", "Modified"])
                
                # Write contacts
                for contact in contacts:
                    writer.writerow([
                        contact["id"],
                        contact["name"],
                        contact.get("email", ""),
                        contact.get("phone", ""),
                        contact.get("notes", ""),
                        contact["created"],
                        contact["modified"]
                    ])
            
            print(f"Contacts exported to {output_file} in CSV format")
            return True
        
        else:
            print(f"Unsupported format: {format}")
            return False
    
    except Exception as e:
        print(f"Error exporting contacts: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Simple Contact Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add contact command
    add_parser = subparsers.add_parser("add", help="Add a new contact")
    add_parser.add_argument("name", help="Contact name")
    add_parser.add_argument("-e", "--email", help="Email address")
    add_parser.add_argument("-p", "--phone", help="Phone number")
    add_parser.add_argument("-n", "--notes", help="Additional notes")
    
    # List contacts command
    list_parser = subparsers.add_parser("list", help="List contacts")
    list_parser.add_argument("-s", "--search", help="Search in contacts")
    
    # View contact command
    view_parser = subparsers.add_parser("view", help="View contact details")
    view_parser.add_argument("id", type=int, help="Contact ID")
    
    # Edit contact command
    edit_parser = subparsers.add_parser("edit", help="Edit a contact")
    edit_parser.add_argument("id", type=int, help="Contact ID")
    edit_parser.add_argument("-n", "--name", help="New name")
    edit_parser.add_argument("-e", "--email", help="New email")
    edit_parser.add_argument("-p", "--phone", help="New phone")
    edit_parser.add_argument("--notes", help="New notes")
    
    # Delete contact command
    delete_parser = subparsers.add_parser("delete", help="Delete a contact")
    delete_parser.add_argument("id", type=int, help="Contact ID")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export contacts to a file")
    export_parser.add_argument("output", help="Output file path")
    export_parser.add_argument("-f", "--format", choices=["json", "csv"], default="json", 
                             help="Export format (default: json)")
    
    # Global options
    parser.add_argument("-f", "--file", default=DEFAULT_CONTACTS_FILE, 
                       help=f"Contacts file (default: {DEFAULT_CONTACTS_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_contact(args.name, args.email, args.phone, args.notes, args.file)
    
    elif args.command == "list":
        list_contacts(args.search, args.file)
    
    elif args.command == "view":
        view_contact(args.id, args.file)
    
    elif args.command == "edit":
        edit_contact(args.id, args.name, args.email, args.phone, args.notes, args.file)
    
    elif args.command == "delete":
        delete_contact(args.id, args.file)
    
    elif args.command == "export":
        export_contacts(args.output, args.format, args.file)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
