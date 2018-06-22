package edu.jaen.control;


import java.util.List;
import java.util.UUID;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothAdapter.LeScanCallback;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;

public class MainActivity extends Activity {
	private final String LOGTAG = "BLECONTROL";
	private BluetoothManager blueMan;
	private BluetoothAdapter blueAdapter;
	private BluetoothGatt gatt;
	private TextView mTv;
	private ListView deviceList;
	private LeDeviceListAdapter mLeDeviceListAdapter;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		mTv = (TextView) findViewById(R.id.mTv);
		blueMan = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
		blueAdapter = blueMan.getAdapter();
		
		deviceList = (ListView) findViewById(R.id.devicelist);
		mLeDeviceListAdapter = new LeDeviceListAdapter(this);
		deviceList.setAdapter(mLeDeviceListAdapter);
	
		deviceList.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				// TODO Auto-generated method stub
				BluetoothDevice device = (BluetoothDevice) mLeDeviceListAdapter.getItem(position);
				gatt = device.connectGatt(getApplicationContext(), false,
						gattCallback);
				h.sendEmptyMessage(CONNECTING);
			}
		});

	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case R.id.action_scan:
			// Toast.makeText(this, "Start Scan", Toast.LENGTH_SHORT).show();
			startScan();
			break;

		case R.id.action_stop:
			// Toast.makeText(this, "Stop Scan", Toast.LENGTH_SHORT).show();
			stopScan();
			break;
		
		case R.id.action_test:
			Toast.makeText(this, "test.... ", Toast.LENGTH_SHORT).show();
			testButton();
//			testButton1();
			testButton2();
			break;
		}
		return super.onOptionsItemSelected(item);
	}

	public void startScan() {
		mLeDeviceListAdapter.clear();
		mLeDeviceListAdapter.notifyDataSetChanged();
		Log.e(LOGTAG, "startScan");
		// BLE Sensor Scan
		blueAdapter.startLeScan(scanCallback);
	}

	private void stopScan() {
		Log.e(LOGTAG, "stopSCan");
		// BLE Sensor Scan Stop
		blueAdapter.stopLeScan(scanCallback);
		if (gatt != null) {
			gatt.disconnect();
			gatt = null;
		}
	}

	BluetoothDevice remoteDevice;
	LeScanCallback scanCallback = new LeScanCallback() {
		@Override
		public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
			// TODO Auto-generated method stub

			if (gatt == null) {
				remoteDevice = device;
				Log.e(LOGTAG, "++++++++++++Device++++++++++++++++++");
				Log.e(LOGTAG, remoteDevice.toString());
				runOnUiThread(new Runnable() {
	                @Override
	                public void run() {
	                    mLeDeviceListAdapter.addDevice(remoteDevice);
	                    mLeDeviceListAdapter.notifyDataSetChanged();
	                }
	            });
			}
		}
	};

	
	BluetoothGattCallback gattCallback = new BluetoothGattCallback() {

		@Override
		public void onConnectionStateChange(BluetoothGatt gatt, int status,
				int newState) {
			// TODO Auto-generated method stub
			super.onConnectionStateChange(gatt, status, newState);
			
			if (newState == BluetoothProfile.STATE_CONNECTED) {
				h.sendEmptyMessage(CONNECTED);
				gatt.discoverServices();
			} else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
				h.sendEmptyMessage(DISCONNECT);
			}
		}

		public void onServicesDiscovered(BluetoothGatt gatt, int status) {
		};

		// gatt.readCharacteristic Callback
		@Override
		public void onCharacteristicRead(BluetoothGatt gatt,
				BluetoothGattCharacteristic ch, int status) {
			Log.e(LOGTAG, "####### onCharacteristicRead");
			if (status == BluetoothGatt.GATT_SUCCESS) {
				getCharacteristic(ch);
			}
		};

		@Override
		public void onReadRemoteRssi(BluetoothGatt gatt, int rssi, int status) {
			if (status == BluetoothGatt.GATT_SUCCESS) {
				Log.e(LOGTAG, "RSSI : " + rssi);
				// h.obtainMessage(RSSI, rssi).sendToTarget();
			}
		};

		public void onCharacteristicChanged(BluetoothGatt gatt,
				BluetoothGattCharacteristic ch) {
			Log.e(LOGTAG, "onCharacteristicChanged========================");
			if (gatt != null) {
				getCharacteristic(ch);
			}
		};

		public void onCharacteristicWrite(BluetoothGatt gatt,
				BluetoothGattCharacteristic characteristic, int status) {
			Log.e(LOGTAG, "onCharacteristicWrite****************************");
		};

		public void onDescriptorWrite(BluetoothGatt gatt,
				BluetoothGattDescriptor descriptor, int status) {

			Log.e(LOGTAG, "onDescriptorWrite------------------------");
			Log.e(LOGTAG, "descriptor : " + descriptor.getUuid()
					+ ", status : " + status);

		};
	};
	String value;
	public void getCharacteristic(BluetoothGattCharacteristic ch) {
		if (blueAdapter == null || gatt == null || ch == null) {
			return;
		}

		UUID uuid = ch.getUuid();

		byte[] rawValue = ch.getValue();

		value = Conversion.BytetohexString(rawValue, rawValue.length);
		runOnUiThread(new Runnable() {
			
			@Override
			public void run() {
				// TODO Auto-generated method stub
				mTv.setText(value);
			}
		});
		if (rawValue.length > 0) {
			Log.e(LOGTAG, "&&&&&&&&&&&&&&&&&&&&&&&&&&&");
			Log.e(value,value);
			Log.e(LOGTAG, "&&&&&&&&&&&&&&&&&&&&&&&&&&&");
		}
	}

	//List<BluetoothGattService> services;
	private final int CONNECTING = 1;
	private final int CONNECTED = 2;
	private final int DISCONNECT = 3;
	private final int RSSI = 4;
	private final int MSG = 5;
	Handler h = new Handler() {
		public void handleMessage(android.os.Message msg) {
			switch (msg.what) {
			case CONNECTING:
				Toast.makeText(getApplicationContext(), "CONNECTING",
						Toast.LENGTH_SHORT).show();
				break;
			case CONNECTED:
				Toast.makeText(getApplicationContext(), "CONNECTED",
						Toast.LENGTH_SHORT).show();
				((TextView)findViewById(R.id.mTv)).setText("BLESensor 에 연결되었습니다.");
				break;
			case DISCONNECT:
				Toast.makeText(getApplicationContext(), "DISCONNECT",
						Toast.LENGTH_SHORT).show();
				((TextView)findViewById(R.id.mTv)).setText("BLESensor 에 연결이 끈어졌습니다.");
				break;
			case RSSI:
				Toast.makeText(getApplicationContext(), "rssi : " + msg.obj,
						Toast.LENGTH_SHORT).show();
				break;
			case MSG:
				Toast.makeText(getApplicationContext(), "info : " + msg.obj,
						Toast.LENGTH_SHORT).show();
				break;
			default:
				break;
			}

		};
	};

	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		stopScan();
	}

	public void sleep(int time) {
		try {
			Thread.sleep(time);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	UUID UUID_ACC_SERV = UUID
			.fromString("f000aa10-0451-4000-b000-000000000000");
	UUID UUID_ACC_DATA = UUID
			.fromString("f000aa11-0451-4000-b000-000000000000");
	UUID UUID_IRT_SERV = UUID
			.fromString("f000aa00-0451-4000-b000-000000000000");
	UUID UUID_IRT_DATA = UUID
			.fromString("f000aa01-0451-4000-b000-000000000000");
	UUID UUID_IRT_CONF = UUID
			.fromString("f000aa02-0451-4000-b000-000000000000");

	UUID UUID_KEY_SERV = UUID
			.fromString("0000ffe0-0000-1000-8000-00805f9b34fb");
	UUID UUID_KEY_DATA = UUID
			.fromString("0000ffe1-0000-1000-8000-00805f9b34fb");

	// ==================================================================
	// mServices.put("f000aa20-0451-4000-b000-000000000000",
	// "SensorTag Humidity Service");
	// mCharacteristics.put("f000aa21-0451-4000-b000-000000000000",
	// "SensorTag Humidity Data");
	// mCharacteristics.put("f000aa22-0451-4000-b000-000000000000",
	// "SensorTag Humidity Config");
	// mCharacteristics.put("f000aa23-0451-4000-b000-000000000000",
	// "SensorTag Humidity Period");

	UUID UUID_HUM_SERV = UUID
			.fromString("f000aa20-0451-4000-b000-000000000000");
	UUID UUID_HIM_DATA = UUID
			.fromString("f000aa21-0451-4000-b000-000000000000");
	UUID UUID_HIM_CONFIG = UUID
			.fromString("f000aa22-0451-4000-b000-000000000000");

	UUID UUID_GYR_SERV = UUID
			.fromString("f000aa50-0451-4000-b000-000000000000");
	UUID UUID_GYR_DATA = UUID
			.fromString("f000aa51-0451-4000-b000-000000000000");
	UUID UUID_GYR_CONFIG = UUID
			.fromString("f000aa52-0451-4000-b000-000000000000");

	private void enableSensor(UUID sevUuid, UUID confUuid) {

		Log.e(LOGTAG, "enableSensor 수행 시작 ------------------");

		BluetoothGattCharacteristic charistic = gatt.getService(sevUuid)
				.getCharacteristic(confUuid);

		byte value = 1;
		byte[] val = new byte[1];
		val[0] = value;
		charistic.setValue(val);
		gatt.writeCharacteristic(charistic);
		
		Log.e(LOGTAG, "enableSensor 수행 완료 ------------------");
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	//온도 테스트
	private void testButton() {
		
		enableSensor(UUID_IRT_SERV, UUID_IRT_CONF);

		BluetoothGattCharacteristic c = gatt.getService(UUID_IRT_SERV).getCharacteristic(UUID_IRT_DATA);
		
		gatt.setCharacteristicNotification(c, true);

		BluetoothGattDescriptor descriptor = c.getDescriptor(UUID
				.fromString("00002902-0000-1000-8000-00805f9b34fb"));


		Log.e(LOGTAG, "testButton 426  descriptor ====: " + descriptor);

		if (descriptor != null) {
			byte[] val = true ? BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
					: BluetoothGattDescriptor.DISABLE_NOTIFICATION_VALUE;
			descriptor.setValue(val);
			gatt.writeDescriptor(descriptor);
		}
		if (c.getValue() != null) {
			Log.d(LOGTAG, "testButton1 501 : " + c.getValue()[0]);
		}
		
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	//자이로스코프 테스트 OK
	private void testButton1() {

		enableSensor(UUID_GYR_SERV, UUID_GYR_CONFIG);

		BluetoothGattCharacteristic c = gatt.getService(UUID_GYR_SERV).getCharacteristic(UUID_GYR_DATA);

		gatt.setCharacteristicNotification(c, true);

		BluetoothGattDescriptor descriptor = c.getDescriptor(UUID
				.fromString("00002902-0000-1000-8000-00805f9b34fb"));

		if (descriptor != null) {
			byte[] val = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE;
			descriptor.setValue(val);
			gatt.writeDescriptor(descriptor);
		}
		if (c.getValue() != null) {
			Log.d(LOGTAG, "testButton1 501 : " + c.getValue()[0]);
		}
		
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	// KEY_DATA 정상적으로 실행됨...
	private void testButton2() {
		BluetoothGattCharacteristic c = null;
		c = gatt.getService(UUID_KEY_SERV).getCharacteristic(UUID_KEY_DATA);
		gatt.setCharacteristicNotification(c, true);
		
		BluetoothGattDescriptor descriptor = c.getDescriptor(UUID
				.fromString("00002902-0000-1000-8000-00805f9b34fb"));

		if (descriptor != null) {
			byte[] val = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE;
			descriptor.setValue(val);
			gatt.writeDescriptor(descriptor);
		}
		
	}
}
