package com.d.smartdoor.smartdoor.services;

import android.content.Context;

import com.amazonaws.mobileconnectors.apigateway.ApiClientFactory;
import com.d.smartdoor.smartdoor.Injection;

import smartdoor.SmartDoorClient;


public class SmartDoorService {

    private SmartDoorClient client;

    public SmartDoorService(Context context) {
        ApiClientFactory factory = Injection.getAWSService().getApiClientFactory();
        client = factory.build(SmartDoorClient.class);
    }

    public SmartDoorClient getSmartDoorClient() {
        return client;
    }

}
