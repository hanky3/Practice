package edu.jaen.network.exam.miband;

import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothAdapter.LeScanCallback;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;
import edu.jaen.network.exam.miband.R;

public class MiActivity extends Activity implements LeScanCallback {

	private BluetoothAdapter mBluetoothAdapter;
	private boolean mScanning;
	private TextView mTextView;
	private Handler mHandler = new Handler();
	// Stops scanning after 10 seconds.
	private static final long SCAN_PERIOD = 30000;
	private String devName;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getActionBar().hide();
		setContentView(R.layout.activity_mi);
		mTextView = (TextView) findViewById(R.id.text_search);
		mBluetoothAdapter = ((BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE))
				.getAdapter();
	}
	
	

	@Override
	public void onResume() {
		super.onResume();
		scanLeDevice(true);
	}

	@SuppressWarnings("deprecation")
	// L Apis are buggy and crap!
	private void scanLeDevice(final boolean enable) {
		if (enable) {
			mTextView.setText(R.string.looking_for_miband);
			// Stops scanning after a pre-defined scan period.
			mHandler.postDelayed(new Runnable() {
				@Override
				public void run() {
					mScanning = false;
					mBluetoothAdapter.stopLeScan(MiActivity.this);
					if(devName==null)
						mTextView.setText(R.string.not_found);
					else
						mTextView.setText("찾은 장비 : "+devName);
				}
			}, SCAN_PERIOD);

			mScanning = true;
			mBluetoothAdapter.startLeScan(this);
		} else {
			mScanning = false;
			mBluetoothAdapter.stopLeScan(this);
		}
	}
	
	public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {
		System.out.println("----- 64 Mac : "+device.toString()+", name : "+device.getName());
		if (device.getAddress().equals("C8:0F:10:0F:35:1D")) {
			//Type 2-> Bluetooth LE 장비
			System.out.println("Name :"+ device.getName()+" type : "+device.getType());
			devName = device.getName()+"  /  MAC : "+device.toString();
			scanLeDevice(false); // we only care about one miband so that's
									// enough
			Intent intent = new Intent(getApplicationContext(), MiOverviewActivity.class);
			intent.putExtra("address", device.getAddress());
			
			startActivity(intent);
			finish();
		}
	}

	//Test 코드 -------
	public void onLeScan_Ori(BluetoothDevice device, int rssi, byte[] scanRecord) {
		System.out.println("----- 64 Mac : "+device.toString()+", name : "+device.getName());
		if (device != null && device.getName() != null
				& device.getName().equals("MI")) {
			System.out.println(device.getAddress());
			scanLeDevice(false); // we only care about one miband so that's
									// enough
			Intent intent = new Intent(getApplicationContext(), MiOverviewActivity.class);
			intent.putExtra("address", device.getAddress());
			//startActivity(intent);
		}
	}
	
	

	@Override
	public void onPause() {
		super.onPause();
		scanLeDevice(false);
	}
}
