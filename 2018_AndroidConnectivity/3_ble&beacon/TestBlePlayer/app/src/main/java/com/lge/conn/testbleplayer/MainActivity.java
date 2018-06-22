package com.lge.conn.testbleplayer;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayInputStream;
import java.util.Formatter;
import java.util.List;
import java.util.UUID;

public class MainActivity extends AppCompatActivity {
    private final String REMOTE_BD_ADDR = "5C:31:3E:BF:FC:30";

    public final UUID UUID_ACC_SERV = UUID.fromString("f000aa10-0451-4000-b000-000000000000");
    public final UUID UUID_ACC_DATA = UUID.fromString("f000aa11-0451-4000-b000-000000000000");
    public final UUID UUID_IRT_SERV = UUID.fromString("f000aa00-0451-4000-b000-000000000000");
    public final UUID UUID_IRT_DATA = UUID.fromString("f000aa01-0451-4000-b000-000000000000");
    public final UUID UUID_IRT_CONF = UUID.fromString("f000aa02-0451-4000-b000-000000000000");
    public final UUID UUID_KEY_SERV = UUID.fromString("0000ffe0-0000-1000-8000-00805f9b34fb");
    public final UUID UUID_KEY_DATA = UUID.fromString("0000ffe1-0000-1000-8000-00805f9b34fb");
    public final UUID UUID_CHAR_DESC = UUID.fromString("00002902-0000-1000-8000-00805f9b34fb");


    private BluetoothAdapter blueAdapter;
    private BluetoothDevice bluetoothDevice;
    private BluetoothGatt blueGatt;

    private TextView infoTv;
    private ScrollView scrollView;

    BluetoothAdapter.LeScanCallback leScanCallback = new BluetoothAdapter.LeScanCallback() {
        @Override
        public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
            if (device.getAddress().equals(REMOTE_BD_ADDR)) {
                sendMessage(">> Device Scan 완료 - " + device);
                bluetoothDevice = device;
                blueAdapter.stopLeScan(leScanCallback);
            }
        }
    };

    ScanCallback leScanCallback2 = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            super.onScanResult(callbackType, result);
        }
    };

    BluetoothGattCallback gattCallback = new BluetoothGattCallback() {
        @Override
        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
            super.onConnectionStateChange(gatt, status, newState);

            if (newState == BluetoothGatt.STATE_CONNECTED) {
                sendMessage(">> Device 연결 완료! - " + gatt.getDevice().toString());
                gatt.discoverServices();
            }
            else if (newState == BluetoothGatt.STATE_DISCONNECTED) {
                sendMessage(">> Device 연결 해제! - " + gatt.getDevice().toString());
            }
        };

        @Override
        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
            super.onServicesDiscovered(gatt, status);
            enableKeyNotification(gatt);
        }

        @Override
        public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic) {
            super.onCharacteristicChanged(gatt, characteristic);

            byte[] data = characteristic.getValue();
            getKeyEventData(characteristic);

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        infoTv = findViewById(R.id.infoTv);
        scrollView = findViewById(R.id.infoScrollView);
        blueAdapter = BluetoothAdapter.getDefaultAdapter();
        bluetoothDevice = null;
        blueGatt = null;
        if (blueAdapter == null) {
            Toast.makeText(this, "Bluetooth 지원하지 않음!!", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        if (!blueAdapter.isEnabled()) {
            Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(intent, 0);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        blueAdapter.stopLeScan(leScanCallback);
        if (blueGatt != null) {
            blueGatt.disconnect();
            blueGatt.close();
        }
    }

    public void onScanStart(View view) {
        sendMessage(">> Scan 시작~~");
        blueAdapter.startLeScan(leScanCallback);
    }

    public void onScanStop(View view) {
        sendMessage(">> Scan 종료~~");
        blueAdapter.stopLeScan(leScanCallback);

        if (blueGatt != null) {
            blueGatt.disconnect();
            blueGatt = null;
        }
    }

    public void onConnect(View view) {
        if (bluetoothDevice == null) {
            Toast.makeText(this, "검색된 Bluetooth Device가 없습니다!!", Toast.LENGTH_SHORT).show();
            return;
        }

        blueGatt = bluetoothDevice.connectGatt(this, false, gattCallback);
    }

    private void sendMessage(String msg) {
        final String data = msg;
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                infoTv.setText(infoTv.getText() + "\n" + data);

                scrollView.post(new Runnable() {
                    @Override
                    public void run() {
                        scrollView.fullScroll(View.FOCUS_DOWN);
                    }
                });
            }
        });
    }

    // KEY_DATA 정상적으로 실행됨...
    private void enableKeyNotification(BluetoothGatt gatt) {
        if (gatt == null) {
            return;
        }

        BluetoothGattCharacteristic c = null;
        c = gatt.getService(UUID_KEY_SERV).getCharacteristic(UUID_KEY_DATA);
        gatt.setCharacteristicNotification(c, true);

        BluetoothGattDescriptor descriptor = c.getDescriptor(UUID_CHAR_DESC);

        if (descriptor != null) {
            byte[] val = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE;
            descriptor.setValue(val);
            gatt.writeDescriptor(descriptor);
            sendMessage(">> KEY_DATA 활성화!!");
        }
    }

    private void getKeyEventData(BluetoothGattCharacteristic ch)
    {
        if (ch == null)
            return;

        String dataStr = BytetohexString(ch.getValue());
        if (dataStr.equals("01")) {
            sendMessage(">> Music Play!!");
            Intent intent = new Intent(this, MyPlayerService.class);
            startService(intent);
        }
        else if(dataStr.equals("02")) {
            sendMessage(">> Music Stop!!");
            Intent intent = new Intent(this, MyPlayerService.class);
            stopService(intent);
        }
    }

    public String BytetohexString(byte[] b) {
        StringBuilder sb = new StringBuilder(b.length * (2 + 1));
        Formatter formatter = new Formatter(sb);

        for (int i = 0; i < b.length; i++) {
            if (i < b.length - 1)
                formatter.format("%02X:", b[i]);
            else
                formatter.format("%02X", b[i]);

        }
        formatter.close();

        return sb.toString();
    }
}
