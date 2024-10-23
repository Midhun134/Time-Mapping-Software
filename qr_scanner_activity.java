// QRScannerActivity.java
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.mlkit.vision.barcode.Barcode;
import com.google.mlkit.vision.barcode.BarcodeScanner;
import com.google.mlkit.vision.barcode.BarcodeScanning;
import com.google.mlkit.vision.barcode.common.Barcode;
import com.google.mlkit.vision.common.InputImage;

import android.graphics.Bitmap;
import android.provider.MediaStore;
import android.content.Intent;
import android.widget.ImageView;
import java.io.IOException;
import java.util.List;

public class QRScannerActivity extends AppCompatActivity {
    private static final int REQUEST_IMAGE_CAPTURE = 1;
    private ImageView qrImageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_qrscanner);

        qrImageView = findViewById(R.id.qrImageView);
        dispatchTakePictureIntent();
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    } 

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            Bitmap imageBitmap = (Bitmap) extras.get("data");
            qrImageView.setImageBitmap(imageBitmap);
            scanQRCode(imageBitmap);
        }
    }

    private void scanQRCode(Bitmap bitmap) {
        InputImage image = InputImage.fromBitmap(bitmap, 0);
        BarcodeScanner scanner = BarcodeScanning.getClient();

        scanner.process(image).addOnCompleteListener(new OnCompleteListener<List<Barcode>>() {
            @Override
            public void onComplete(@NonNull Task<List<Barcode>> task) {
                if (task.isSuccessful()) {
                    List<Barcode> barcodes = task.getResult();
                    for (Barcode barcode : barcodes) {
                        String rawValue = barcode.getRawValue();
                        Toast.makeText(QRScannerActivity.this, "QR Code: " + rawValue, Toast.LENGTH_LONG).show();
                    }
                } else {
                    Toast.makeText(QRScannerActivity.this, "Failed to scan QR code", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}

// AndroidManifest.xml should include the permissions for using the camera:
// <uses-permission android:name="android.permission.CAMERA" />
// <uses-feature android:name="android.hardware.camera" android:required="true" />