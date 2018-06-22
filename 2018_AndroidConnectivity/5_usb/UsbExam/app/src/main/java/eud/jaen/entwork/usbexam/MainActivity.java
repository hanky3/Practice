package eud.jaen.entwork.usbexam;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.hardware.usb.UsbDevice;
import android.hardware.usb.UsbManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.hoho.android.usbserial.driver.UsbSerialDriver;
import com.hoho.android.usbserial.driver.UsbSerialProber;

public class MainActivity extends Activity {
    Button btnOn = null;
    Button btnOff = null;
    TextView txt = null;
    UsbDevice arduino = null;
    UsbSerialDriver driver = null;
    boolean isRun = true;

    @SuppressLint("NewApi")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.layout_main);
        btnOn = (Button) findViewById(R.id.btnOn);
        btnOff = (Button) findViewById(R.id.btnOff);
        txt = (TextView) findViewById(R.id.text);

        View.OnClickListener listener = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (driver != null) {
                    try {
                        if (v.getId() == R.id.btnOn) {
                            Log.d("aurduino", "On Send");
                            driver.write("1".getBytes(), 1000);
                        } else {
                            Log.d("aurduino", "Off Send");
                            driver.write("0".getBytes(), 1000);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        btnOn.setOnClickListener(listener);
        btnOff.setOnClickListener(listener);
        UsbManager manager = (UsbManager) getSystemService(Context.USB_SERVICE); // UsbManager를
                                                                                    // System으로
                                                                                    // 부터
                                                                                    // get
        HashMap<String, UsbDevice> deviceList = manager.getDeviceList(); // 연결된
                                                                            // device
                                                                            // 목록
                                                                            // 추
        System.out.println("==================== 69");
        Set<String> deviceNames = deviceList.keySet();
        System.out.println("=====================71 size : "+deviceNames.size());
        for (Iterator<String> iterator = deviceNames.iterator(); iterator
                .hasNext();) {
            String name = iterator.next();
            UsbDevice device = deviceList.get(name);
            String deviceName = device.getDeviceName();
            int deviceId = device.getDeviceId();
            int deviceProtocol = device.getDeviceProtocol();
            int productId = device.getProductId();
            int vendorId = device.getVendorId();
            System.out.println("==================== arduino name : "+name+", vender Id :"+vendorId);
            Log.d("arduino", "name :" + name + ", devceName :" + deviceName
                    + "+deviceId:" + deviceId + ", procol: " + deviceProtocol
                    + " ,productId:" + productId + ", vendorId:" + vendorId);
            if (device.getVendorId() == 9025) {
                arduino = device;
                driver = UsbSerialProber.acquire(manager, arduino);
                // List<UsbSerialDriver> drivers =
                // UsbSerialProber.probeSingleDevice(manager, arduino);
                // if(drivers != null && drivers.size() > 0){
                // Log.d("arduino", "drivers size :" + drivers.size());
                // driver = drivers.get(0);
                // }
                break;
            }
        }

        if (driver != null) {
            try {
                driver.open();
                driver.setBaudRate(9600);
                // driver.setParameters(9600, 8, UsbSerialDriver.STOPBITS_1,
                // UsbSerialDriver.PARITY_NONE);
                myTask.execute();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
    }

    @Override
    protected void onDestroy() {
        // TODO Auto-generated method stub
        super.onDestroy();
        isRun = false;
        myTask.cancel(true);
    }

    AsyncTask<Void, String, Void> myTask = new AsyncTask<Void, String, Void>() {
        byte[] read = new byte[128];
        byte[] buff = new byte[128];
        int buffCnt = 0;

        @Override
        protected Void doInBackground(Void... params) {
            try {
                while (isRun) {
                    Arrays.fill(read, (byte) 0);
                    int readCnt = driver.read(read, 100);
                    Log.d("arduino", "read(" + readCnt + ")"
                            + new String(read, 0, readCnt));
                    for (int i = 0; i < readCnt; i++) {
                        if (read[i] == 13) {
                            String msg = new String(buff, 0, buffCnt);
                            Arrays.fill(buff, (byte) 0);
                            buffCnt = 0;
                            publishProgress(msg);
                        } else if (read[i] != 10) {
                            if (buffCnt >= buff.length) {
                                Arrays.fill(buff, (byte) 0);
                            }
                            buff[buffCnt++] = read[i];
                        }
                    }
                    Thread.sleep(200);
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            } catch (InterruptedException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            txt.append(values[0] + "\n");
            Log.d("arduino", values[0]);
        }
    };
}