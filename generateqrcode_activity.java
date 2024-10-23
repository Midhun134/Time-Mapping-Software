//Code to send the request from android application to the backend server
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class GenerateQRCodeActivity extends AppCompatActivity {
    private EditText dataInput;
    private Button generateButton;
    private final OkHttpClient client = new OkHttpClient();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_generate_qr);

        dataInput = findViewById(R.id.dataInput);
        generateButton = findViewById(R.id.generateButton);

        generateButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String data = dataInput.getText().toString();
                if (!data.isEmpty()) {
                    sendPostRequest(data);
                } else {
                    Toast.makeText(GenerateQRCodeActivity.this, "Please enter data", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }

    private void sendPostRequest(String data) {
        RequestBody formBody = new FormBody.Builder()
                .add("data", data)
                .build();

        Request request = new Request.Builder()
                .url("http://<YOUR_SERVER_IP>:<PORT>/generate_qr/") // Replace with your Django server IP and PORT
                .post(formBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("GenerateQRCodeActivity", "Failed to send request", e);
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String responseBody = response.body().string();
                    Log.d("GenerateQRCodeActivity", "QR Code generated: " + responseBody);
                    // You can also parse JSON response and provide feedback to the user.
                } else {
                    Log.e("GenerateQRCodeActivity", "Server error: " + response.code());
                }
            }
        });
    }
}
