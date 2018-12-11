package com.d.smartdoor.smartdoor.services;

import android.content.Context;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.mobile.auth.core.IdentityManager;
import com.amazonaws.mobile.config.AWSConfiguration;
import com.amazonaws.mobile.auth.userpools.CognitoUserPoolsSignInProvider;
import com.amazonaws.mobileconnectors.apigateway.ApiClientFactory;
import com.d.smartdoor.smartdoor.Injection;

public class AWSService {
    private AWSConfiguration awsConfiguration;
    private IdentityManager identityManager;
    private ApiClientFactory factory;

    public AWSService(Context context) {
        awsConfiguration = new AWSConfiguration(context);
        identityManager = new IdentityManager(context, awsConfiguration);
        identityManager.addSignInProvider(CognitoUserPoolsSignInProvider.class);
        IdentityManager.setDefaultIdentityManager(identityManager);
        factory = new ApiClientFactory();
    }

    public IdentityManager getIdentityManager() {
        return identityManager;
    }

    public AWSConfiguration getConfiguration() {
        return awsConfiguration;
    }

    public ApiClientFactory getApiClientFactory() {
        return factory;
    }
}