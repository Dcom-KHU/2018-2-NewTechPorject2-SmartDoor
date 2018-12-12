package com.d.smartdoor.smartdoor.services;

import android.content.Context;
import android.util.Log;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.mobile.api.idssfdn56nqg.SmartDoorClient;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobileconnectors.apigateway.ApiClientFactory;
import com.d.smartdoor.smartdoor.Injection;

public class SmartDoorService {

    private SmartDoorClient client;

    public SmartDoorService(Context context) {

        client = new ApiClientFactory()
                .credentialsProvider(Injection.getAWSService().getIdentityManager().getCredentialsProvider())
                .build(SmartDoorClient.class);
    }

    public SmartDoorClient getSmartDoorClient() {
        return client;
    }

}
