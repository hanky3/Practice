package edu.jaen.blescan;

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
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
	private final String LOGTAG = "BLESCAN";
	private BluetoothManager blueMan;
	private BluetoothAdapter blueAdapter;
	private TextView tv;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		tv = (TextView) findViewById(R.id.tv);
		blueMan = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
		blueAdapter = blueMan.getAdapter();

	}
	
	@Override
	protected void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
		if(!blueAdapter.isEnabled()){
			Intent i = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
			startActivityForResult(i, 0);
		}
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
		blueAdapter.startLeScan(scanCallback);
	}

	private void stopScan() {
		Log.e(LOGTAG, "stopScan");
		blueAdapter.stopLeScan(scanCallback);
	}

	BluetoothDevice remoteDevice;
	LeScanCallback scanCallback = new LeScanCallback() {
		@Override
		public void onLeScan(final BluetoothDevice device, int rssi,
				byte[] scanRecord) {
			remoteDevice = device;
			Log.e(LOGTAG, "++++++++++++Device++++++++++++++++++");
			Log.e(LOGTAG, "addr : " + remoteDevice.toString());
			runOnUiThread(new Runnable() {

				@Override
				public void run() {
					// TODO Auto-generated method stub
					tv.setText("addr : " + remoteDevice.toString() + "\n");
				}
			});
			try {
				Thread.sleep(30);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	};

	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		stopScan();
	}
}
