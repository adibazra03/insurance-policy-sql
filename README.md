# Insurance Policy Management System

A web application built with Flask and Oracle Database for managing insurance policies, customers, and related data.

## Features

- **Customer Management**: Add, edit, remove, and search customers
- **Policy Management**: Add, edit, remove, and search insurance policies
- **Policy Types**: Support for car, home, and life insurance policies
- **Database Integration**: Uses Oracle Database for data persistence
- **Web Interface**: User-friendly HTML templates for all operations

## Prerequisites

- Python 3.x
- Access to Oracle Database (hosted at Penn State)
- VPN connection required for off-campus access

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd insurance-policy-sql
   ```

2. Install dependencies:
   ```bash
   pip install flask oracledb
   ```

## Usage

1. **Connect to Penn State Network**:
   - If off-campus, connect to the **GlobalProtect VPN** before running the app.

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open your browser and go to: `http://127.0.0.1:5000`

4. **Stop the Application**:
   - Press `Ctrl + C` in the terminal where the app is running.

## Database

- **Schema**: Defined in `db/schema.sql`
- **Sample Data**: Available in `db/sample_data.sql`
- **Connection**: Requires Oracle Database access through Penn State network

## Project Structure

```
insurance-policy-sql/
├── app.py                 # Main Flask application
├── main.py                # Entry point
├── addMethods.py          # Methods for adding records
├── removeMethods.py       # Methods for removing records
├── searchMethods.py       # Methods for searching records
├── displayMethods.py      # Methods for displaying data
├── buildTable.py          # Database table building utilities
├── insertData.py          # Data insertion utilities
├── db/
│   ├── schema.sql         # Database schema
│   └── sample_data.sql    # Sample data
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── customers_list.html
│   ├── customer_add.html
│   ├── customer_edit.html
│   ├── customer_remove.html
│   ├── customer_search.html
│   ├── policies_list.html
│   ├── policy_add.html
│   ├── policy_edit.html
│   ├── policy_remove.html
│   ├── policy_search.html
│   ├── car_policies.html
│   ├── home_policies.html
│   └── life_policies.html
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes.
