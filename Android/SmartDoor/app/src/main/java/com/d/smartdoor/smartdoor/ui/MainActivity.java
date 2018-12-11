package com.d.smartdoor.smartdoor.ui;

import android.os.AsyncTask;
import android.os.Bundle;
import android.os.ResultReceiver;
import android.service.media.MediaBrowserService;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.amazonaws.http.HttpMethodName;
import com.amazonaws.mobileconnectors.apigateway.ApiRequest;
import com.amazonaws.mobileconnectors.apigateway.ApiResponse;
import com.d.smartdoor.smartdoor.Injection;
import com.d.smartdoor.smartdoor.R;

import javax.xml.transform.Result;

import smartdoor.SmartDoorClient;
import smartdoor.model.Empty;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button openButton = findViewById(R.id.openButton);

        openButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("API", "button Pushed");
                RunApi runApi = new RunApi();
                runApi.execute();

            }
        });

    }
}

class RunApi extends AsyncTask<String, Void, String> {
    @Override
    protected String doInBackground(String... voids) {
        SmartDoorClient client = Injection.getSmartDoorService().getSmartDoorClient();

        ApiRequest request = new ApiRequest("doors");
        request.withHttpMethod(HttpMethodName.GET);
        ApiResponse response = null;

        try {
            response = client.execute(request);
            Log.d("POST", response.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }

        String message = "";
        if (response == null) {
            message = "Error";
        } else {
            message = "Opened";
        }
        Log.d("API", message);
        return message;
    }
}
