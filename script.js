// Simple Login Function
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    if (username === "admin" && password === "password123") {
        document.getElementById('loginMessage').innerText = "Login successful!";
    } else {
        document.getElementById('loginMessage').innerText = "Invalid credentials!";
    }
});

// Job Registration Function
document.getElementById('jobForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let vehicleNumber = document.getElementById('vehicleNumber').value;
    let jobDescription = document.getElementById('jobDescription').value;

    document.getElementById('jobMessage').innerText = `Job for vehicle ${vehicleNumber} registered successfully!`;
});

// Vehicle Tracking Function
function trackVehicle() {
    let vehicleNumber = document.getElementById('trackingNumber').value;
    document.getElementById('trackingResult').innerText = `Vehicle ${vehicleNumber} is currently being serviced.`;
}

// Job Details Search Function
function searchJob() {
    let vehicleNumber = document.getElementById('searchJob').value;
    document.getElementById('jobResult').innerText = `Job details for vehicle ${vehicleNumber} are available.`;
}
// QR Code Scanner for Job Entry/Exit
function setupQrCodeScanner() {
    function onScanSuccess(decodedText, decodedResult) {
        // Handle the QR code data (e.g., vehicle number)
        let vehicleNumber = decodedText;

        // Redirect to start or end job based on the QR code result
        window.location.href = `/start-job/${vehicleNumber}/`;  // Modify this URL based on your logic
    }

    let html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", { fps: 10, qrbox: 250 });
    html5QrcodeScanner.render(onScanSuccess);
}

// Ensure the function is called when needed, e.g., when the QR code scanner div is loaded
document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("qr-reader")) {
        setupQrCodeScanner();
    }
});
