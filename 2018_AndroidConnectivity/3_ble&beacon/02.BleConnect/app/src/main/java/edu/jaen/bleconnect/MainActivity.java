package edu.jaen.bleconnect;

import static java.util.UUID.fromString;

import java.util.ArrayList;
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
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity extends Activity {
	private final String LOGTAG = "BLECONNECT";
	private BluetoothManager blueMan;
	private BluetoothAdapter blueAdapter;
	private BluetoothGatt gatt;
	private ListView deviceList;
	private ListView serviceList;
	private ListView charList;
	private LeDeviceListAdapter mLeDeviceListAdapter;
	private LeServiceListAdapter serviceAdapter;
	private ArrayAdapter<String> charAdapter;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		deviceList = (ListView) findViewById(R.id.devicelist);
		blueMan = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
		blueAdapter = blueMan.getAdapter();
		
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
        
        serviceList = (ListView) findViewById(R.id.servicelist);
        serviceAdapter = new LeServiceListAdapter(this);
        serviceList.setAdapter(serviceAdapter);
        serviceList.setOnItemClickListener(new OnItemClickListener() {

			@Override
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id) {
				// TODO Auto-generated method stub
				charAdapter.clear();
				BluetoothGattService service = serviceAdapter.getService(position);
				List<BluetoothGattCharacteristic> characteristics = service.getCharacteristics();
				for (BluetoothGattCharacteristic c : characteristics) {
					charAdapter.add(c.getUuid().toString());
				}
				charAdapter.notifyDataSetChanged();
			}
		});
        
        charList = (ListView) findViewById(R.id.charlist);
        charAdapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1);
        charList.setAdapter(charAdapter);
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
		}
		return super.onOptionsItemSelected(item);
	}

	public void startScan() {
		mLeDeviceListAdapter.clear();
		mLeDeviceListAdapter.notifyDataSetChanged();
		Log.e(LOGTAG, "startScan");
		blueAdapter.startLeScan(scanCallback);
	}

	private void stopScan() {
		Log.e(LOGTAG, "stopSCan");
		blueAdapter.stopLeScan(scanCallback);

		if (gatt != null) {
			gatt.disconnect();
			gatt = null;
			 Toast.makeText(this, "disconnect.... ",
			 Toast.LENGTH_SHORT).show();
		}
	}

	BluetoothDevice remoteDevice;
	LeScanCallback scanCallback = new LeScanCallback() {
		@Override
		public void onLeScan(final BluetoothDevice device, int rssi, byte[] scanRecord) {
			// TODO Auto-generated method stub
			if (gatt == null) {
				remoteDevice = device;
				Log.e(LOGTAG, "++++++++++++Device++++++++++++++++++");
				Log.e(LOGTAG, remoteDevice.toString());
				
				runOnUiThread(new Runnable() {
	                @Override
	                public void run() {
	                    mLeDeviceListAdapter.addDevice(device);
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
		ArrayList<BluetoothGattService> temp = new ArrayList<BluetoothGattService>();
		public void onServicesDiscovered(BluetoothGatt gatt, int status) {
			services = gatt.getServices();
			temp.clear();
			for (BluetoothGattService service : services) {
				temp.add(service);
				String serviceUuid = service.getUuid().toString();
				Log.e(LOGTAG, "---------------------------------------");
				Log.e(LOGTAG, "service UUID : " + serviceUuid);
				List<BluetoothGattCharacteristic> characteristics = service
						.getCharacteristics();
				
				for (BluetoothGattCharacteristic c : characteristics) {
					String charUuid = c.getUuid().toString();
					sleep(100);
					Log.e(LOGTAG, "C UUID : " + charUuid);

				}
				
			}
			runOnUiThread(new Runnable() {
				
				@Override
				public void run() {
					// TODO Auto-generated method stub
					serviceAdapter.clear();
					serviceAdapter.addAll(temp);
					serviceAdapter.notifyDataSetChanged();
				}
			});
		};

		// gatt.readCharacteristic Callback
		@Override
		public void onCharacteristicRead(BluetoothGatt gatt,
				BluetoothGattCharacteristic ch, int status) {
			
		};

		@Override
		public void onReadRemoteRssi(BluetoothGatt gatt, int rssi, int status) {
			if (status == BluetoothGatt.GATT_SUCCESS) {
				// we got new value of RSSI of the connection, pass it to the UI
				Log.e(LOGTAG, "RSSI : " + rssi);
				//h.obtainMessage(RSSI, rssi).sendToTarget();
			}
		};

		public void onCharacteristicChanged(BluetoothGatt gatt,
				BluetoothGattCharacteristic ch) {
			Log.e(LOGTAG, "onCharacteristicChanged");
			
		};
	};

	List<BluetoothGattService> services;
	private final int CONNECTING = 1;
	private final int CONNECTED = 2;
	private final int DISCONNECT = 3;
	private final int RSSI = 4;
	private int count = 0;
	
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
				break;
			case DISCONNECT:
				Toast.makeText(getApplicationContext(), "DISCONNECT",
						Toast.LENGTH_SHORT).show();
				break;
			case RSSI:
				Toast.makeText(getApplicationContext(), "rssi : " + msg.obj,
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
}
