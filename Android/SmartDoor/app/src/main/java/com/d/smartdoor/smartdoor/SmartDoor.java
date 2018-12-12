package com.d.smartdoor.smartdoor;

import android.app.Activity;
import android.os.Bundle;
import android.support.multidex.MultiDexApplication;

public class SmartDoor extends MultiDexApplication {

    public static String APP = "app";

    @Override
    public void onCreate() {
        super.onCreate();
        Injection.initialize(getApplicationContext());
    }
}