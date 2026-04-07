# Information Security Policy
**Effective Date:** January 1, 2026  
**Version:** 4.0  
**Document Owner:** Chief Information Security Officer (CISO)  
**Classification:** Internal Use Only

---

## Table of Contents
1. [Policy Overview](#policy-overview)
2. [Access Control](#access-control)
3. [Data Classification](#data-classification)
4. [Password Management](#password-management)
5. [Endpoint Security](#endpoint-security)
6. [Network Security](#network-security)
7. [Incident Response](#incident-response)
8. [Third-Party Security](#third-party-security)
9. [Security Training](#security-training)

---

## Policy Overview

### Purpose
This Information Security Policy establishes the framework for protecting Quantic AI Engineering's information assets, including data, systems, networks, and intellectual property. The policy ensures confidentiality, integrity, and availability of information while supporting business objectives.

### Scope
This policy applies to:
- All employees (full-time, part-time, contract)
- Consultants and temporary workers
- Business partners with access to company systems
- All information systems, networks, and data owned or managed by the company
- All devices connecting to company networks or accessing company data

### Compliance Requirements
This policy supports compliance with:
- General Data Protection Regulation (GDPR)
- California Consumer Privacy Act (CCPA)
- SOC 2 Type II requirements
- ISO 27001 standards
- Industry-specific regulations applicable to our clients

### Violations
Non-compliance with this policy may result in:
- Disciplinary action up to and including termination
- Legal action for serious violations
- Mandatory security retraining
- Loss of system access privileges
- Financial penalties where applicable

---

## Access Control

### Principle of Least Privilege
Users shall be granted the minimum level of access necessary to perform their job functions. Access rights must be:
- Justified by business need
- Approved by data owner and supervisor
- Reviewed quarterly
- Revoked immediately upon role change or termination

### User Account Management

**Account Creation:**
- Accounts created only upon receipt of approved access request
- Unique username assigned to each individual
- No shared accounts (except approved service accounts)
- Default access level is "read-only" unless higher access justified

**Account Review:**
- Manager reviews direct reports' access quarterly
- HR triggers review upon role changes
- Unused accounts disabled after 30 days of inactivity
- Disabled accounts deleted after 90 days

**Account Termination:**
- Access revoked immediately upon termination or resignation
- Manager notifies IT and Security on employee's last day
- All credentials disabled within 2 hours
- Equipment retrieved and wiped within 5 business days

### Authentication Requirements

**User Authentication:**
- Multi-factor authentication (MFA) required for all accounts
- MFA methods: authenticator app, hardware token, or biometric
- SMS-based MFA discouraged due to security concerns
- Backup authentication method must be registered

**Session Management:**
- Automatic logout after 15 minutes of inactivity
- Screen lock required when leaving workstation
- Concurrent sessions limited to 3 devices
- Remote sessions must use VPN

### Privileged Access
Users with administrative privileges must:
- Use separate admin accounts (not regular user accounts)
- Enable MFA with hardware token (Yubikey or similar)
- Document all privileged actions in change log
- Complete annual advanced security training
- Undergo enhanced background screening

---

## Data Classification

### Classification Levels

**PUBLIC:**
- Information intended for public disclosure
- Marketing materials, press releases, public website content
- No protection requirements beyond basic integrity
- Examples: blog posts, product brochures

**INTERNAL:**
- Information for internal use only
- Business-as-usual documents and communications
- Standard protection: password-protected, encrypted in transit
- Examples: internal memos, org charts, project plans

**CONFIDENTIAL:**
- Sensitive business information
- Unauthorized disclosure could harm company
- Enhanced protection: encryption at rest and in transit, access logging
- Examples: financial data, unreleased products, strategic plans

**RESTRICTED:**
- Highly sensitive or regulated information
- Unauthorized disclosure could cause severe harm or legal liability
- Maximum protection: strong encryption, access auditing, DLP monitoring
- Examples: customer PII, trade secrets, source code, security credentials

### Handling Requirements

**Confidential Data:**
- Store only on approved company systems
- Encrypt files before email transmission
- Use secure file sharing (SharePoint, encrypted links)
- Redact or mask data when possible for non-production use
- Never store on personal devices or cloud services

**Restricted Data:**
- Store only in approved secure repositories
- Require explicit approval for each access grant
- Use data loss prevention (DLP) tools
- Log all access and modifications
- Prohibit email transmission unless encrypted and approved
- Destroy securely when no longer needed (per retention policy)

### Data Retention and Destruction

**Retention Periods:**
- Financial records: 7 years
- Personnel files: 7 years after separation
- Contracts: Duration + 7 years
- Email: 3 years unless legally required to retain
- Security logs: 1 year minimum

**Secure Destruction:**
- Digital: Use approved secure deletion tools (minimum 3-pass overwrite)
- Physical: Shred documents (cross-cut, <4mm particles)
- Disposal certificates required for Restricted data
- Hard drives must be degaussed or physically destroyed

---

## Password Management

### Password Requirements

**Complexity:**
- Minimum 14 characters
- Mix of uppercase, lowercase, numbers, and symbols
- No dictionary words or common patterns
- No personal information (names, birthdates)
- Passphrases encouraged (e.g., "Coffee!Morning@2026#Startup")

**Expiration:**
- Standard accounts: change every 90 days
- Privileged accounts: change every 60 days
- System prompts for change 7 days before expiration
- Cannot reuse last 10 passwords

**Service Accounts:**
- Minimum 20 characters, randomly generated
- Stored in approved password vault (HashiCorp Vault)
- Changed every 180 days or upon personnel change
- Access to service account passwords logged

### Password Manager
- Company-provided password manager: 1Password Enterprise
- Required for all employees
- Master password must meet enhanced standards (20+ characters)
- Enable MFA for password manager access
- Store all work-related passwords in password manager

### Prohibited Practices
- Writing passwords down (except in sealed envelope stored in safe)
- Sharing passwords with colleagues
- Using same password across multiple systems
- Storing passwords in browsers
- Sending passwords via email or chat
- Including passwords in scripts or configuration files

---

## Endpoint Security

### Company Devices

**Device Management:**
- All company devices must be enrolled in MDM (Microsoft Intune)
- Full disk encryption required (BitLocker for Windows, FileVault for Mac)
- Automatic security updates enabled
- Anti-malware software installed and active
- Personal use permitted within reasonable limits

**Security Requirements:**
- Screen lock password: minimum 10 characters or 6-digit PIN with biometric
- Lock automatically after 5 minutes idle
- Biometric authentication (fingerprint/facial recognition) encouraged
- Remote wipe capability must remain enabled
- Location services enabled for lost device recovery

**Software Installation:**
- Only approved software may be installed
- Request software through IT ServiceNow portal
- No unauthorized cloud storage services (Dropbox, Google Drive personal)
- Prohibited: P2P software, game clients, cryptocurrency miners

### Personal Devices (BYOD)

**Permitted Use:**
- Email access via mobile device with Company Portal app
- Calendar and contacts synchronization
- Microsoft Teams for chat and calls
- View-only access to SharePoint documents

**Security Requirements:**
- Device PIN/password required
- Encryption enabled
- Latest OS version (or one version behind)
- Mobile Device Management (MDM) enrollment required
- Company data containerized and separate from personal data

**Prohibited Use:**
- Downloading Restricted or Confidential files
- Using personal cloud storage for work files
- Jailbroken or rooted devices
- Devices shared with family members

### Physical Security
- Never leave devices unattended in public places
- Lock laptop to desk with cable lock when in office
- Do not check laptop as airline baggage
- Report lost or stolen devices immediately (within 1 hour)
- Use privacy screen in public spaces

---

## Network Security

### Corporate Network Access
- Wired connections preferred for sensitive work
- Wi-Fi uses WPA3 encryption with 802.1X authentication
- Guest network isolated from corporate network
- Network access control (NAC) enforces compliance

### Remote Access
- VPN required for all remote connections to corporate resources
- Split-tunneling disabled (all traffic routes through VPN)
- VPN uses IKEv2 with AES-256 encryption
- Automatic VPN reconnection on connection drop
- VPN access logged and audited

### Wi-Fi Security
**Corporate Wi-Fi:**
- Separate SSIDs for corporate and guest access
- Corporate SSID requires certificate-based authentication
- Guest access requires registration and acceptance of terms
- Guest sessions limited to 8 hours

**Public Wi-Fi:**
- Prohibited for accessing company resources without VPN
- Use mobile hotspot when available
- Assume all public networks are compromised
- Disable automatic connection to open networks

### Firewall and IDS/IPS
- Host-based firewall required on all endpoints
- Intrusion detection system monitors network traffic
- Suspicious activity generates alerts to Security Operations Center
- Automated blocking of known malicious IP addresses

---

## Incident Response

### Reporting Requirements

**Security Incidents Include:**
- Suspected malware infection
- Phishing or social engineering attempts
- Lost or stolen devices
- Unauthorized access to systems or data
- Data breaches or leaks
- Suspicious system behavior
- Policy violations

**Reporting Process:**
1. Immediately contact Security Operations Center (SOC):
   - Email: security@quanticai.com
   - Phone: 1-800-555-SECURE (available 24/7)
   - Teams: @SecurityTeam
2. Do NOT attempt to investigate or remediate yourself
3. Preserve evidence (don't delete emails, don't reboot systems)
4. Document what happened: timeline, actions taken, people involved
5. Follow instructions from security team

**Reporting Timeline:**
- Critical incidents (data breach, ransomware): Immediately
- High severity (compromised account): Within 1 hour
- Medium severity (suspicious email): Within 4 hours
- Low severity (policy questions): Within 24 hours

### Incident Response Process

**1. Detection and Reporting:**
- User reports incident or automated system detects anomaly
- SOC analyst triages and assigns severity level

**2. Containment:**
- Isolate affected systems from network
- Disable compromised accounts
- Block malicious IP addresses or domains
- Preserve evidence for investigation

**3. Investigation:**
- Determine scope and impact
- Identify root cause
- Document findings
- Assess data exposure

**4. Eradication:**
- Remove malware or unauthorized access
- Patch vulnerabilities
- Reset compromised credentials
- Restore systems from clean backups if necessary

**5. Recovery:**
- Restore normal operations
- Monitor for recurrence
- Validate system integrity

**6. Post-Incident:**
- Conduct lessons learned meeting
- Update security controls
- Provide remedial training if needed
- Document incident in security log

### Data Breach Notification
If personal data breach occurs:
- Privacy team notified within 2 hours
- Affected individuals notified within 72 hours (GDPR requirement)
- Regulatory agencies notified per legal requirements
- Public disclosure if risk of harm to individuals
- Credit monitoring offered if appropriate

---

## Third-Party Security

### Vendor Risk Assessment
Before engaging any vendor with access to company data or systems:
- Complete vendor security questionnaire
- Review SOC 2 or ISO 27001 certification
- Assess data handling and security practices
- Include security requirements in contract
- Obtain cyber liability insurance proof

### Third-Party Access
Vendors granted system access must:
- Use unique, named accounts (no shared credentials)
- Enable MFA on all accounts
- Access granted for limited time period
- Activity monitored and logged
- Access reviewed quarterly and revoked when no longer needed

### Data Sharing with Third Parties
- Execute Data Processing Agreement (DPA) before sharing data
- Share minimum necessary data
- Classify data and apply appropriate protections
- Use secure transfer methods (SFTP, encrypted email)
- Verify recipient's identity before transfer
- Log all data transfers

---

## Security Training

### Required Training

**New Employee Orientation:**
- Security awareness training within first week
- Policy acknowledgment required before system access
- Phishing simulation within first 30 days

**Annual Training:**
- Refresher training required each January
- Covers current threats and updated policies
- Completion tracked; non-compliance escalated to manager

**Role-Specific Training:**
- Developers: Secure coding practices (annual)
- Privileged users: Advanced security training (annual)
- Managers: Data classification and handling (annual)

### Phishing Simulations
- Monthly simulated phishing campaigns
- Clicking malicious link triggers immediate training module
- Repeat offenders receive one-on-one training
- Aggregate results reported to leadership (not individual names)

### Security Awareness
- Monthly security newsletter with tips and threat updates
- Quarterly "lunch and learn" sessions on security topics
- Security awareness posters throughout office
- Recognition program for reporting phishing attempts

---

## Policy Enforcement

### Monitoring and Auditing
- Security team monitors systems for policy compliance
- Random audits of user activity and access
- Automated alerts for suspicious behavior
- Annual comprehensive security audit

### Non-Compliance Consequences

**First Violation:**
- Warning and remedial training
- Manager notification
- Documented in employee file

**Second Violation:**
- Formal written warning
- Performance improvement plan
- Temporary suspension of system access privileges

**Third Violation or Serious Breach:**
- Termination of employment
- Legal action if applicable
- Law enforcement notification for criminal activity

### Policy Exceptions
- Exceptions must be formally requested through security team
- Business justification required
- CISO approval mandatory
- Compensating controls implemented
- Exception documented and reviewed annually

---

## Policy Review

This policy is reviewed annually and updated as needed to address emerging threats and business changes. Last review: December 15, 2025. Next scheduled review: December 2026.

---

## Acknowledgment

I acknowledge that I have read, understood, and agree to comply with the Information Security Policy. I understand that violations may result in disciplinary action including termination and legal consequences.

**Employee Name:** _______________________________

**Signature:** _______________________________

**Date:** _______________________________

---

*For questions about this policy, contact the Security Team at security@quanticai.com or extension 5200.*
