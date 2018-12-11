package com.d.smartdoor.smartdoor;

import android.content.Context;

import com.d.smartdoor.smartdoor.services.AWSService;

public class Injection {

    private static AWSService awsService = null;

    public static synchronized AWSService getAWSService() {
        return awsService;
    }

    public static synchronized void initialize(Context context) {
        if (awsService == null) {
            awsService = new AWSService(context);
        }
    }
}
