package com.d.smartdoor.smartdoor.services;

import android.content.Context;
import android.util.Log;

import com.amazonaws.auth.CognitoCachingCredentialsProvider;
import com.amazonaws.auth.CognitoCredentialsProvider;
import com.amazonaws.mobile.auth.core.IdentityManager;
import com.amazonaws.mobile.auth.userpools.CognitoUserPoolsSignInProvider;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobile.client.AWSStartupHandler;
import com.amazonaws.mobile.client.AWSStartupResult;
import com.amazonaws.mobile.config.AWSConfiguration;
import com.amazonaws.mobileconnectors.apigateway.ApiClientFactory;
import com.amazonaws.mobileconnectors.cognitoidentityprovider.CognitoUserPool;

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
        factory.credentialsProvider(identityManager.getCredentialsProvider());
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