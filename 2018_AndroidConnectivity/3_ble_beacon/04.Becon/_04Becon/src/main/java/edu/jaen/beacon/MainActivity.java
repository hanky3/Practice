package edu.jaen.beacon;

import uk.co.alt236.bluetoothlelib.device.BluetoothLeDevice;
import uk.co.alt236.bluetoothlelib.device.IBeaconDevice;
import uk.co.alt236.bluetoothlelib.device.mfdata.IBeaconManufacturerData;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.os.Bundle;
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
	private final String LOGTAG = "BEACON";
	private BluetoothManager blueMan;
	private BluetoothAdapter blueAdapter;
	private BluetoothGatt gatt;
	private TextView mTv;
	private ListView deviceList;
	private LeDeviceListAdapter mLeDeviceListAdapter;
	private String addr;

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
				BluetoothDevice device = (BluetoothDevice) mLeDeviceListAdapter
						.getItem(position);
				addr = device.toString();
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
		}
		return super.onOptionsItemSelected(item);
	}

	public void startScan() {
		Log.e(LOGTAG, "startScan");
		mLeDeviceListAdapter.clear();
		mLeDeviceListAdapter.notifyDataSetChanged();
		// IBeacon Sensor Scan
		blueAdapter.startLeScan(mLeScanCallback);

	}

	private void stopScan() {
		Log.e(LOGTAG, "stopSCan");

		// IBeacon Sensor Scan
		blueAdapter.stopLeScan(mLeScanCallback);

	}

	BluetoothDevice remoteDevice;

	// ======================IBeacon 용 LeScanCallback=======================

	private BluetoothAdapter.LeScanCallback mLeScanCallback = new BluetoothAdapter.LeScanCallback() {
		private int tx;
		private int major;
		private int minor;
		private double distance;

		public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
			remoteDevice = device;
			// TODO Auto-generated method stub
			runOnUiThread(new Runnable() {
				@Override
				public void run() {
					mLeDeviceListAdapter.addDevice(remoteDevice);
					mLeDeviceListAdapter.notifyDataSetChanged();
				}
			});
			if (device.toString().equals(addr)) {
				final BluetoothLeDevice deviceLe = new BluetoothLeDevice(
						device, rssi, scanRecord, System.currentTimeMillis());
				try {

					Log.e(LOGTAG, "Device " + deviceLe.getAddress()
							+ " updated.");

					IBeaconManufacturerData iBeaconData = new IBeaconManufacturerData(
							deviceLe);
					tx = iBeaconData.getCalibratedTxPower();
					major = iBeaconData.getMajor();
					minor = iBeaconData.getMinor();
					// distance = (float) rssi / (float) tx;
					distance = Math.pow(12.0,
							1.5 * (((float) rssi / (float) tx) - 1));

					System.out.println("rssi : " + rssi + ", tx : " + tx
							+ ", =====거리 : " + distance);

					runOnUiThread(new Runnable() {

						@Override
						public void run() {
							// TODO Auto-generated method stub
							mTv.setText("Major : " + major + ", Minor " + minor
									+ ", distance : " + distance);
						}
					});
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}

	};

	// IOS 거리 계산 공식 : 값이 많이 튐
	private double calculateAccuracy(int txPower, double rssi) {

		if (rssi == 0) {
			return -1.0; // if we can not determine accuracy, return -1.
		}

		double ratio = rssi * 1.0 / txPower;
		if (ratio < 1.0) {
			return Math.pow(ratio, 10);
		} else {
			double accuracy = (0.89976) * Math.pow(ratio, 7.7095) + 0.111;
			return accuracy;
		}
	}

	private double getNewAccuracy(int txPower, double rssi) {
		return Math.pow(12.0, 1.5 * ((rssi / txPower) - 1));
	}
}
