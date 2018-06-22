package com.lge.conn.testble;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattServer;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothProfile;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

public class MainActivity extends AppCompatActivity {

    private EditText macEditTxt;
    private TextView statusTv;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothDevice remoteDevice;
    private BluetoothGatt bluetoothGatt;
    private String devMacAddr;

    BluetoothAdapter.LeScanCallback scanCallback = new BluetoothAdapter.LeScanCallback() {
        @Override
        public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
            Log.e("INFO", "----------"+device.getAddress());

            if (devMacAddr.equals(device.getAddress())) {
                remoteDevice = device;
                bluetoothAdapter.stopLeScan(scanCallback);
                showMessage(remoteDevice+" Scan 완료......");
            }
        }
    };

    BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            super.onConnectionStateChange(gatt, status, newState);

            if (newState == BluetoothProfile.STATE_CONNECTED) {
                Log.e("INFO", "Sensor와 연결 완료...");

                showMessage("Sensor와 연결 완료...");
                bluetoothGatt.discoverServices();
                showMessage("Sensor 서비스 검색 시작!!...");
            }
            else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                Log.e("INFO", "Sensor와 연결 끊김...");
                showMessage("Sensor와 연결 끊김...");
                bluetoothGatt = null;
            }

        }

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            super.onServicesDiscovered(gatt, status);
            List<BluetoothGattService> gattServiceList = gatt.getServices();

            showMessage("Sensor 서비스 검색 완료!!...");
            for (BluetoothGattService s : gattServiceList) {
                showMessage("=>" + s.getUuid());
                for (BluetoothGattCharacteristic c : s.getCharacteristics()) {
                    showMessage("===>" + c.getUuid());
                }
            }
        }

        @Override
        public void onCharacteristicRead(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
            super.onCharacteristicRead(gatt, characteristic, status);
        }

        @Override
        public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status) {
            super.onCharacteristicWrite(gatt, characteristic, status);
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
            super.onCharacteristicChanged(gatt, characteristic);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        if (bluetoothAdapter == null) {
            Toast.makeText(this, "Bluetooth 지원 안됨", Toast.LENGTH_SHORT).show();
            finish();
        }

        macEditTxt = findViewById(R.id.editText);
        statusTv = findViewById(R.id.statusTv);
        statusTv.setMovementMethod(new ScrollingMovementMethod());
        remoteDevice = null;
        bluetoothGatt = null;

    }

    @Override
    protected void onResume() {
        super.onResume();

        if (!bluetoothAdapter.isEnabled()) {
            Intent i = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(i, 0);
        }
    }

    public void registerDevice(View view) {
        devMacAddr = macEditTxt.getText().toString();
        showMessage(devMacAddr + "장비 등록 완료");
    }

    public void onScanStart(View view) {
        bluetoothAdapter.startLeScan(scanCallback);
        showMessage("scan Start.......");
    }

    public void onScanStop(View view) {
        bluetoothAdapter.stopLeScan(scanCallback);
        showMessage("scan Stop.......");
    }

    public void onConnect(View view) {
        if (remoteDevice == null)
            return;

        bluetoothGatt = remoteDevice.connectGatt(this, false, gattCallback);
        showMessage("start Connecting device(" + remoteDevice + ").......");
    }

    private void showMessage(String msg) {
        final String data = msg;
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                statusTv.setText(statusTv.getText()+"\n" + data);
            }
        });
    }
}
