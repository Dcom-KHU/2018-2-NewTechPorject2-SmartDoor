package com.example.admin.bea;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.RemoteException;
import android.support.annotation.Nullable;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.altbeacon.beacon.Beacon;
import org.altbeacon.beacon.BeaconConsumer;
import org.altbeacon.beacon.BeaconManager;
import org.altbeacon.beacon.BeaconParser;
import org.altbeacon.beacon.MonitorNotifier;
import org.altbeacon.beacon.RangeNotifier;
import org.altbeacon.beacon.Region;
import org.altbeacon.beacon.utils.UrlBeaconUrlCompressor;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity implements BeaconConsumer {
    protected  static final String TAG = "RangingActivity";
    private BeaconManager beaconManager;
    public String msgList = "X";
    private SharedPreferences registered_device ;


    private static final int REQUEST_ENABLE_BT = 10; // 블루투스 활성화 상태
    private int pariedDeviceCount;
    private BluetoothAdapter bluetoothAdapter; // 블루투스 어댑터
    private Set<BluetoothDevice> devices; // 블루투스 디바이스 데이터 셋
    private BluetoothDevice bluetoothDevice; // 블루투스 디바이스


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter(); // 블루투스 어댑터를 디폴트 어댑터로 설정
        if(bluetoothAdapter == null) { // 디바이스가 블루투스를 지원하지 않을 때
            finish();// 여기에 처리 할 코드를 작성하세요.
        }
        else { // 디바이스가 블루투스를 지원 할 때
            if(bluetoothAdapter.isEnabled()) { // 블루투스가 활성화 상태 (기기에 블루투스가 켜져있음)
                registered_device = getSharedPreferences("registered_device", MODE_PRIVATE);
                String info = registered_device.getString("MAC","");
                if(info.equals("")){
                    Toast.makeText(getApplicationContext(),"value",Toast.LENGTH_SHORT ).show();
                    SelectBluetoothDevice();
                }
               // SelectBluetoothDevice();
            }
            else { // 블루투스가 비 활성화 상태 (기기에 블루투스가 꺼져있음)
                // 블루투스를 활성화 하기 위한 다이얼로그 출력
                Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                // 선택한 값이 onActivityResult 함수에서 콜백된다.
                startActivityForResult(intent, REQUEST_ENABLE_BT);
            }
        }



        // findViewById(R.id.get_beacon_info).setOnClickListener(btn1);

            beaconManager = BeaconManager.getInstanceForApplication(this);
        beaconManager.getBeaconParsers().add(new BeaconParser().setBeaconLayout("s:0-1=feaa,m:2-2=10,p:3-3:-41,i:4-20v"));
            beaconManager.bind(this);

            findViewById(R.id.get_beacon_info).setOnClickListener(btn1);

    }

    Button.OnClickListener btn1 = new View.OnClickListener(){

        @Override
        public void onClick(View v) {
            Toast.makeText(getApplicationContext(),msgList,Toast.LENGTH_SHORT ).show();
        }
    };


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case REQUEST_ENABLE_BT :
                if(requestCode == RESULT_OK) { // '사용'을 눌렀을 때
                    registered_device = getSharedPreferences("registered_device", MODE_PRIVATE);
                    String info = registered_device.getString("MAC","");
                    if(info.equals("")){
                        Toast.makeText(getApplicationContext(),"value",Toast.LENGTH_SHORT ).show();
                        SelectBluetoothDevice();
                    }
                }
                else { // '취소'를 눌렀을 때
                    finish();// 여기에 처리 할 코드를 작성하세요.
                }
                break;
        }
    }


    @Override
    protected void onDestroy() {
        super.onDestroy();
        beaconManager.unbind(this);
    }

    @Override
    public void onBeaconServiceConnect() {
        beaconManager.addRangeNotifier(new RangeNotifier()
        {
            @Override
            public void didRangeBeaconsInRegion(Collection beacons, Region region)
            {
                if (beacons.size() > 0)
                {
                    Log.e(TAG, "The first beacon I see is about "

                            +((Beacon)beacons.iterator().next()).getDistance()+" meters away." + ((Beacon)beacons.iterator().next()).getId1() + ":::::");
                    String msg = "Beacon name: " + ((Beacon)beacons.iterator().next()).getBluetoothName() + "Beacon Distance: " +((Beacon)beacons.iterator().next()).getDistance()+" meters away.";
                   // Toast.makeText(getApplicationContext(),msg,Toast.LENGTH_SHORT ).show();
                   // msgList.add(msg);

                    String Mac_address = registered_device.getString("MAC","" );

                    if(((Beacon)beacons.iterator().next()).getBluetoothAddress().equals(Mac_address)) {
                        if(msgList.equals("X"))
                            msgList = msg;
                        Log.e(TAG, "IT is coorrect!!");
                        Beacon rpibeacon = ((Beacon)beacons.iterator().next());
                        String url = UrlBeaconUrlCompressor.uncompress(rpibeacon.getId1().toByteArray());
                        Log.d(TAG, "I see a beacon transmitting a url: " + url +
                                " approximately " + rpibeacon.getDistance() + " meters away.");

                    }
                }
            }
        });
        try
        {
            beaconManager.startRangingBeaconsInRegion(

                    new Region("65194", null, null, null));
        }
        catch (RemoteException e)
        {
        }
    }

    public void SelectBluetoothDevice() {
        // 이미 페어링 되어있는 블루투스 기기를 찾습니다.
        devices = bluetoothAdapter.getBondedDevices();
        // 페어링 된 디바이스의 크기를 저장
        pariedDeviceCount = devices.size();
        // 페어링 되어있는 장치가 없는 경우
        if (pariedDeviceCount == 0) {
            // 페어링을 하기위한 함수 호출
        }
        // 페어링 되어있는 장치가 있는 경우
        else {
            // 디바이스를 선택하기 위한 다이얼로그 생성
            AlertDialog.Builder builder = new AlertDialog.Builder(this);
            builder.setTitle("페어링 되어있는 블루투스 디바이스 목록");
            // 페어링 된 각각의 디바이스의 이름과 주소를 저장
            List<String> list = new ArrayList<>();
            // 모든 디바이스의 이름을 리스트에 추가
            for (BluetoothDevice bluetoothDevice : devices) {
                list.add(bluetoothDevice.getName());

            }
            list.add("취소");

            // List를 CharSequence 배열로 변경
            final CharSequence[] charSequences = list.toArray(new CharSequence[list.size()]);
            list.toArray(new CharSequence[list.size()]);
            // 해당 아이템을 눌렀을 때 호출 되는 이벤트 리스너

            builder.setItems(charSequences, new DialogInterface.OnClickListener() {

                @Override
                public void onClick(DialogInterface dialog, int which) {
                    // 해당 디바이스와 연결하는 함수 호출
                     connectDevice(charSequences[which].toString());
                }

            });


            AlertDialog alertDialog = builder.create();

            alertDialog.show();


        }
    }

    public void connectDevice(String deviceName) {
        // 이미 페어링 되어있는 블루투스 기기를 찾습니다.
        devices = bluetoothAdapter.getBondedDevices();
        // 페어링 된 디바이스의 크기를 저장
        pariedDeviceCount = devices.size();
        // 페어링 되어있는 장치가 없는 경우

        // 페어링 된 디바이스들을 모두 탐색
        for (BluetoothDevice tempDevice : devices) {
            // 사용자가 선택한 이름과 같은 디바이스로 설정하고 반복문 종료
            if (deviceName.equals(tempDevice.getName())) {
                bluetoothDevice = tempDevice;
                SharedPreferences.Editor editor = registered_device.edit();
                editor.putString("MAC", tempDevice.getAddress());
                editor.apply();
                break;
            }
        }
    }




    }
