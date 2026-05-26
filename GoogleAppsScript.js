/**
 * Google Apps Script for Financing Obligation Tracker
 * 
 * This script monitors a Google Drive folder for new PDF files
 * and automatically sends them to the Vercel API for processing.
 * 
 * SETUP INSTRUCTIONS:
 * 1. Open Google Drive
 * 2. Create a folder for financing agreements (e.g., "Financing Agreements")
 * 3. Copy the folder ID from the URL
 * 4. Go to https://script.google.com
 * 5. Create new project
 * 6. Paste this code
 * 7. Update CONFIG below with your values
 * 8. Run "setup" function once to authorize
 * 9. Set up trigger: Edit → Current project's triggers → Add trigger
 *    - Choose function: checkForNewPDFs
 *    - Event source: Time-driven
 *    - Type: Minutes timer
 *    - Interval: Every 10 minutes (or hourly)
 */

// ============================================================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================================================

const CONFIG = {
  // Your Google Drive folder ID (from folder URL)
  DRIVE_FOLDER_ID: '1C5CPeXuTEJkGpGtHPpChYV0f7VoQdPBI',
  
  // Your Vercel API endpoint (use production domain, not deployment-specific URL)
  API_ENDPOINT: 'https://financing-obligation-tracker.vercel.app/api/sync/google-drive',
  
  // API secret (same as CRON_SECRET in Vercel)
  API_SECRET: '9dad96e393b29aad6af49f5777bc97a135d4e0ac107a8be050ed91116ae527b1',
  
  // Email to send notifications to
  NOTIFICATION_EMAIL: 'coorpjames@gmail.com'
};

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

/**
 * Check for new PDF files in the monitored folder.
 * This function is called by the time-driven trigger.
 */
function checkForNewPDFs() {
  try {
    Logger.log('=== Starting PDF check ===');
    Logger.log('Time: ' + new Date());
    
    // Get the monitored folder
    const folder = DriveApp.getFolderById(CONFIG.DRIVE_FOLDER_ID);
    Logger.log('Monitoring folder: ' + folder.getName());
    
    // Get last check time from script properties
    const scriptProperties = PropertiesService.getScriptProperties();
    const lastCheckTime = scriptProperties.getProperty('lastCheckTime');
    const lastCheck = lastCheckTime ? new Date(lastCheckTime) : new Date(0);
    
    Logger.log('Last check: ' + lastCheck);
    
    // Find new PDF files
    const files = folder.getFilesByType(MimeType.PDF);
    const newFiles = [];
    
    while (files.hasNext()) {
      const file = files.next();
      const fileModified = file.getLastUpdated();
      
      if (fileModified > lastCheck) {
        newFiles.push(file);
        Logger.log('Found new file: ' + file.getName());
      }
    }
    
    Logger.log('Total new files: ' + newFiles.length);
    
    // Process each new file
    if (newFiles.length > 0) {
      processNewFiles(newFiles);
      
      // Update last check time
      scriptProperties.setProperty('lastCheckTime', new Date().toISOString());
    } else {
      Logger.log('No new files to process');
    }
    
    Logger.log('=== PDF check completed ===');
    
  } catch (error) {
    Logger.log('ERROR: ' + error.toString());
    sendErrorNotification(error);
  }
}

/**
 * Process new PDF files by sending them to the API.
 */
function processNewFiles(files) {
  const results = [];
  
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    Logger.log('Processing: ' + file.getName());
    
    try {
      // Get file content as base64
      const blob = file.getBlob();
      const base64 = Utilities.base64Encode(blob.getBytes());
      
      // Prepare payload
      const payload = {
        filename: file.getName(),
        fileId: file.getId(),
        content: base64,
        mimeType: file.getMimeType(),
        size: file.getSize(),
        modifiedTime: file.getLastUpdated().toISOString()
      };
      
      // Send to API
      const response = callAPI(payload);
      
      if (response.success) {
        Logger.log('✅ Successfully processed: ' + file.getName());
        results.push({
          filename: file.getName(),
          status: 'success',
          message: response.message
        });
        
        // Move file to "Processed" subfolder (optional)
        // moveToProcessedFolder(file, folder);
        
      } else {
        Logger.log('❌ Failed to process: ' + file.getName());
        Logger.log('Error: ' + response.error);
        results.push({
          filename: file.getName(),
          status: 'error',
          message: response.error
        });
      }
      
    } catch (error) {
      Logger.log('❌ Error processing ' + file.getName() + ': ' + error.toString());
      results.push({
        filename: file.getName(),
        status: 'error',
        message: error.toString()
      });
    }
  }
  
  // Send summary notification
  if (results.length > 0) {
    sendSummaryNotification(results);
  }
}

/**
 * Call the Vercel API endpoint.
 */
function callAPI(payload) {
  try {
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Bearer ' + CONFIG.API_SECRET
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };
    
    const response = UrlFetchApp.fetch(CONFIG.API_ENDPOINT, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();
    
    Logger.log('API Response Code: ' + responseCode);
    Logger.log('API Response: ' + responseText);
    
    if (responseCode === 200) {
      return JSON.parse(responseText);
    } else {
      return {
        success: false,
        error: 'API returned status ' + responseCode + ': ' + responseText
      };
    }
    
  } catch (error) {
    return {
      success: false,
      error: error.toString()
    };
  }
}

/**
 * Move processed file to "Processed" subfolder.
 */
function moveToProcessedFolder(file, parentFolder) {
  try {
    // Get or create "Processed" subfolder
    const processedFolders = parentFolder.getFoldersByName('Processed');
    let processedFolder;
    
    if (processedFolders.hasNext()) {
      processedFolder = processedFolders.next();
    } else {
      processedFolder = parentFolder.createFolder('Processed');
    }
    
    // Move file
    file.moveTo(processedFolder);
    Logger.log('Moved to Processed folder: ' + file.getName());
    
  } catch (error) {
    Logger.log('Error moving file: ' + error.toString());
  }
}

/**
 * Send summary email notification.
 */
function sendSummaryNotification(results) {
  try {
    const successCount = results.filter(r => r.status === 'success').length;
    const errorCount = results.filter(r => r.status === 'error').length;
    
    const subject = `📊 Financing Tracker: ${successCount} processed, ${errorCount} errors`;
    
    let body = '<html><body style="font-family: Arial, sans-serif;">';
    body += '<h2>Google Drive Sync Summary</h2>';
    body += `<p>Time: ${new Date().toLocaleString()}</p>`;
    body += `<p><strong>Total files:</strong> ${results.length}</p>`;
    body += `<p><strong>Successful:</strong> ${successCount}</p>`;
    body += `<p><strong>Errors:</strong> ${errorCount}</p>`;
    body += '<hr>';
    body += '<h3>Details:</h3>';
    body += '<ul>';
    
    results.forEach(result => {
      const icon = result.status === 'success' ? '✅' : '❌';
      body += `<li>${icon} <strong>${result.filename}</strong>: ${result.message}</li>`;
    });
    
    body += '</ul>';
    body += '</body></html>';
    
    MailApp.sendEmail({
      to: CONFIG.NOTIFICATION_EMAIL,
      subject: subject,
      htmlBody: body
    });
    
    Logger.log('Summary notification sent');
    
  } catch (error) {
    Logger.log('Error sending notification: ' + error.toString());
  }
}

/**
 * Send error notification email.
 */
function sendErrorNotification(error) {
  try {
    const subject = '❌ Financing Tracker: Script Error';
    const body = `
      <html><body style="font-family: Arial, sans-serif;">
        <h2>Google Apps Script Error</h2>
        <p><strong>Time:</strong> ${new Date().toLocaleString()}</p>
        <p><strong>Error:</strong></p>
        <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">${error.toString()}</pre>
        <p>Please check the script logs for more details.</p>
      </body></html>
    `;
    
    MailApp.sendEmail({
      to: CONFIG.NOTIFICATION_EMAIL,
      subject: subject,
      htmlBody: body
    });
    
  } catch (e) {
    Logger.log('Error sending error notification: ' + e.toString());
  }
}

// ============================================================================
// SETUP FUNCTIONS
// ============================================================================

/**
 * Initial setup function.
 * Run this once to authorize the script and test the configuration.
 */
function setup() {
  Logger.log('=== Running Setup ===');
  
  // Test Drive access
  try {
    const folder = DriveApp.getFolderById(CONFIG.DRIVE_FOLDER_ID);
    Logger.log('✅ Drive folder found: ' + folder.getName());
  } catch (error) {
    Logger.log('❌ Error accessing Drive folder: ' + error.toString());
    Logger.log('Please check your DRIVE_FOLDER_ID in CONFIG');
    return;
  }
  
  // Test API endpoint
  try {
    const testPayload = {
      test: true,
      message: 'Setup test from Google Apps Script'
    };
    
    const response = callAPI(testPayload);
    Logger.log('API test response: ' + JSON.stringify(response));
    
  } catch (error) {
    Logger.log('❌ Error testing API: ' + error.toString());
    Logger.log('Please check your API_ENDPOINT and API_SECRET in CONFIG');
    return;
  }
  
  // Initialize last check time
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty('lastCheckTime', new Date().toISOString());
  Logger.log('✅ Last check time initialized');
  
  Logger.log('=== Setup Complete ===');
  Logger.log('Next steps:');
  Logger.log('1. Go to Edit → Current project\'s triggers');
  Logger.log('2. Add trigger for checkForNewPDFs function');
  Logger.log('3. Set to run every 10 minutes or hourly');
}

/**
 * Manual test function.
 * Run this to manually check for new files.
 */
function manualTest() {
  Logger.log('=== Manual Test ===');
  checkForNewPDFs();
}

/**
 * Reset last check time (useful for testing).
 */
function resetLastCheckTime() {
  const scriptProperties = PropertiesService.getScriptProperties();
  scriptProperties.setProperty('lastCheckTime', new Date(0).toISOString());
  Logger.log('Last check time reset to epoch');
}
