package com.d.smartdoor.smartdoor.ui;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.amazonaws.http.HttpMethodName;
import com.amazonaws.mobileconnectors.apigateway.ApiRequest;
import com.amazonaws.mobileconnectors.apigateway.ApiResponse;
import com.d.smartdoor.smartdoor.Injection;
import com.d.smartdoor.smartdoor.R;

import smartdoor.SmartDoorClient;

public class MainActivity extends AppCompatActivity {

    TextView textView;
    ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button openButton = findViewById(R.id.openButton);
        textView = findViewById(R.id.textView);
        progressBar = findViewById(R.id.progressBar);

        openButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("API", "button Pushed");
                RunApi runApi = new RunApi();
                runApi.execute();

            }
        });

    }

    class RunApi extends AsyncTask<String, Void, ApiResponse> {

        SmartDoorClient client;

        @Override
        protected void onPreExecute() {
            client = Injection.getSmartDoorService().getSmartDoorClient();
            progressBar.setVisibility(View.VISIBLE);
            textView.setText("Requested.");
        }

        @Override
        protected ApiResponse doInBackground(String... params) {

            ApiRequest request = new ApiRequest("/doors");
            request.withHttpMethod(HttpMethodName.GET);
            ApiResponse response = null;

            try {
                response = client.execute(request);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return response;
        }

        @Override
        protected void onProgressUpdate(Void... values) {

        }

        @Override
        protected void onPostExecute(ApiResponse apiResponse) {
            progressBar.setVisibility(View.GONE);
            textView.setText(apiResponse.getStatusText());
        }
    }
}

