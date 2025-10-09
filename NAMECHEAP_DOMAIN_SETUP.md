# Domain Verification Guide for Namecheap + Google Cloud

## Step 1: Google Cloud Domain Verification

### 1.1 Open Google Cloud Console Domain Verification
1. Go to: https://console.cloud.google.com/apis/credentials/domainverification
2. Make sure your project "orchestratex" is selected
3. Click "Add Domain"
4. Enter: `orchestratex.me`
5. Click "Add Domain"

### 1.2 Get the TXT Record
Google will provide a TXT record like:
```
Type: TXT
Name: @ (or orchestratex.me)
Value: google-site-verification=ABC123XYZ456...
```

## Step 2: Add TXT Record in Namecheap

### 2.1 Login to Namecheap
1. Go to: https://www.namecheap.com
2. Login to your account
3. Go to "Domain List" or "Manage Domains"

### 2.2 Access DNS Settings
1. Find "orchestratex.me" in your domain list
2. Click "Manage" next to the domain
3. Click "Advanced DNS" tab

### 2.3 Add the TXT Record
1. In the "Host Records" section, click "Add New Record"
2. Select "TXT Record" from the dropdown
3. Fill in:
   - **Type:** TXT
   - **Host:** @ (or leave blank)
   - **Value:** Paste the google-site-verification value from Google Cloud
   - **TTL:** Automatic (or 1 min for faster propagation)
4. Click "Save All Changes"

## Step 3: Verify Domain in Google Cloud

### 3.1 Wait and Verify
1. Wait 5-15 minutes for DNS propagation
2. Go back to Google Cloud Domain Verification console
3. Click "Verify" next to your domain
4. If successful, you'll see a green checkmark

### 3.2 Check Verification Status
```powershell
# Check if domain is verified
gcloud domains list-user-verified-domains
```

## Step 4: Set up Cloud Run Domain Mapping

Once verified, run:
```powershell
# Create domain mapping
gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region asia-south1
```

## Step 5: Configure DNS Records for Cloud Run

After domain mapping is created, you'll get DNS records like:
```
Type: A
Name: @ (or orchestratex.me)
Value: 216.239.32.21

Type: A
Name: @ (or orchestratex.me)
Value: 216.239.34.21

Type: A
Name: @ (or orchestratex.me)
Value: 216.239.36.21

Type: A
Name: @ (or orchestratex.me)
Value: 216.239.38.21

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:32::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:34::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:36::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:38::15
```

### 5.1 Add These Records in Namecheap
For each A record:
1. Click "Add New Record"
2. Type: A Record
3. Host: @ (or leave blank)
4. Value: [IP address from Google]
5. TTL: Automatic

For each AAAA record:
1. Click "Add New Record"
2. Type: AAAA Record
3. Host: @ (or leave blank)
4. Value: [IPv6 address from Google]
5. TTL: Automatic

## Step 6: Optional - Add WWW Subdomain

Add a CNAME record for www:
- **Type:** CNAME
- **Host:** www
- **Value:** orchestratex.me
- **TTL:** Automatic

## Timeline

- **TXT Record Propagation:** 5-60 minutes
- **Domain Verification:** Immediate after propagation
- **A/AAAA Record Propagation:** 5-60 minutes
- **SSL Certificate:** 5-15 minutes after DNS propagation

## Troubleshooting

### Check DNS Propagation
```bash
nslookup orchestratex.me
nslookup orchestratex.me 8.8.8.8
```

### Online DNS Check Tools
- https://whatsmydns.net
- https://dnschecker.org

### Common Issues
1. **Verification fails:** Wait longer for DNS propagation
2. **Wrong TXT value:** Copy the exact value from Google Cloud
3. **TTL too high:** Set to 1 minute for faster propagation
4. **Wrong host:** Use @ or leave blank for root domain