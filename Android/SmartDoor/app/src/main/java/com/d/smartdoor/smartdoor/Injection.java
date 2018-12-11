package com.d.smartdoor.smartdoor;

import android.content.Context;

import com.d.smartdoor.smartdoor.services.AWSService;
import com.d.smartdoor.smartdoor.services.SmartDoorService;

public class Injection {

    private static AWSService awsService = null;
    private static SmartDoorService smartDoorService = null;

    public static synchronized AWSService getAWSService() {
        return awsService;
    }

    public static synchronized SmartDoorService getSmartDoorService() {
        return smartDoorService;
    }

    public static synchronized void initialize(Context context) {
        if (awsService == null) {
            awsService = new AWSService(context);
        }
        if (smartDoorService == null) {
            smartDoorService = new SmartDoorService(context);
        }
    }
}
