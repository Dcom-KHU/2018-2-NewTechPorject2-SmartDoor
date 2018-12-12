package com.d.smartdoor.smartdoor.ui;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.amazonaws.http.HttpMethodName;
import com.amazonaws.mobile.api.idssfdn56nqg.SmartDoorClient;
import com.amazonaws.mobileconnectors.apigateway.ApiRequest;
import com.amazonaws.mobileconnectors.apigateway.ApiResponse;
import com.d.smartdoor.smartdoor.Injection;
import com.d.smartdoor.smartdoor.R;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class MainActivity extends AppCompatActivity {

    TextView textView;
    ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button openButton = findViewById(R.id.openButton);
        Button doorsButton = findViewById(R.id.doorsButton);
        textView = findViewById(R.id.textView);
        progressBar = findViewById(R.id.progressBar);

        openButton.setOnClickListener(mOnClickListener);
        doorsButton.setOnClickListener(mOnClickListener);
    }

    private View.OnClickListener mOnClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            String path="", method="";
            switch (v.getId()){
                case R.id.openButton:
                    path = "doors/test/open";
                    method = "post";
                    break;
                case R.id.doorsButton:
                    path = "doors";
                    method = "get";
                    break;
            }

            RunApi runApi = new RunApi();
            runApi.execute(path, method);
        }
    };

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

            ApiRequest request = new ApiRequest(client.getClass().getSimpleName())
                    .withPath(params[0])
                    .addHeader("Content-Type", "application/json");
            switch (params[1]) {
                case "get":
                    request.withHttpMethod(HttpMethodName.GET);
                    break;
                case "post":
                    request.withHttpMethod(HttpMethodName.POST);
                    break;
                case "put":
                    request.withHttpMethod(HttpMethodName.PUT);
                    break;
            }
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
            String responseBody = "empty";
            try {
                responseBody = convertStreamToString(apiResponse.getRawContent());
            } catch (IOException e) {
                e.printStackTrace();
            }

            textView.setText(responseBody);
        }

        private String convertStreamToString(InputStream is) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            StringBuilder sb = new StringBuilder();

            String line = null;
            try {
                while ((line = reader.readLine()) != null) {
                    sb.append(line).append('\n');
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    is.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return sb.toString();
        }
    }
}

