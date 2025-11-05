# Rubrik Daily Health Check

A comprehensive Python application that monitors and reports on the health of your Rubrik environment. The tool collects data about clusters, live mounts, data sources, and generates detailed reports in Excel format with optional Google Drive integration.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- 🔍 **Comprehensive Health Monitoring**
  - Cluster status and compliance
  - Live mount tracking (Oracle, MSSQL, VM, Managed Volumes)
  - Data source connectivity (Windows, Linux, NAS hosts)
  - Backup job status and performance

- 📊 **Automated Reporting**
  - Excel reports with detailed metrics
  - Customizable time zones
  - Optional Google Drive integration
  - Cluster-level filtering

- 🔒 **Secure Authentication**
  - Rubrik Security Cloud (RSC) integration
  - Service account support
  - Token-based authentication

## Prerequisites

- Python 3.9.1 or higher
- Access to Rubrik Security Cloud (RSC)
- Network connectivity to Rubrik CDM clusters

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/leonardobesen/rubrik-daily-check.git
   cd rubrik-daily-check
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Rubrik Configuration (Required)

Create `configuration/config.json`:

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "name": "automation_account_name",
  "access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
  "graphql_url": "https://yourdomain.my.rubrik.com/api/graphql",
  "google_drive_upload_folder_ids": ["folder_id_1", "folder_id_2"],
  "tz_info": "America/Sao_Paulo",
  "excluded_clusters_uuids": ["cluster_uuid_1", "cluster_uuid_2"]
}
```

#### Optional Parameters

- **tz_info**: Time zone for reports (default: UTC)
- **google_drive_upload_folder_ids**: Google Drive folders for report upload
- **excluded_clusters_uuids**: Clusters to exclude from health checks

### 2. Google Drive Integration (Optional)

If using Google Drive upload, create `configuration/google_drive.json`:

```json
{
  "installed": {
    "client_id": "your_google_client_id",
    "project_id": "your_project_id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your_google_client_secret",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Usage

1. Ensure configuration files are in place
2. Run the health check:

   ```bash
   python main.py
   ```

The script will:

1. Connect to your Rubrik environment
2. Collect health metrics
3. Generate an Excel report
4. Upload to Google Drive (if configured)

Reports are saved in the `reports` directory with the naming format: `Rubrik_Environment_Health_Check_DD-MM-YYYY_HH_MM_SS.xlsx`

## Output Example

The generated report includes:

- Cluster health status
- Live mount details
- Host connectivity status
- Backup job statistics
- Compliance metrics

## Error Handling

The application includes robust error handling and logging:

- Connection issues are logged with detailed error messages
- Data collection failures are handled gracefully
- Google Drive upload errors are reported clearly

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions:

- Open an [Issue](https://github.com/leonardobesen/rubrik-daily-check/issues)
- Submit a [Pull Request](https://github.com/leonardobesen/rubrik-daily-check/pulls)
