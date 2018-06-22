package com.jaen.o2o.jaenpay.beacon;

import com.jaen.o2o.jaenpay.R;
import com.jaen.o2o.jaenpay.util.CommonUtilities;

import uk.co.alt236.bluetoothlelib.device.BluetoothLeDevice;
import uk.co.alt236.bluetoothlelib.device.mfdata.IBeaconManufacturerData;
import android.app.AlertDialog;
import android.app.Service;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.media.AudioManager;
import android.media.SoundPool;
import android.net.Uri;
import android.os.IBinder;
import android.util.Log;
import android.widget.Toast;

import static android.content.Intent.FLAG_ACTIVITY_NEW_TASK;

public class BeaconService extends Service {

	private final static int BEACON_MAJOR = 36757;
	private final static int BEACON_MINOR = 15036;

	private BluetoothAdapter blueAdapter;
	private BluetoothDevice remoteDevice;
	private boolean isFrist = true;
	private String className;
	private SoundPool soundPool;
	private int sound;

	@Override
	public void onCreate() {
		// TODO Auto-generated method stub
		super.onCreate();
		Log.e(this.getClass().getSimpleName(), "BeaconService onCreate");

		//BluetoothAdpater 객체를 가져온다. ..

		//코드 구현 ------------
        blueAdapter = BluetoothAdapter.getDefaultAdapter();
        if (blueAdapter == null) {
            Toast.makeText(this, "Bluetooth 지원하지 않음!!", Toast.LENGTH_SHORT).show();
            stopSelf();
        }

		soundPool = new SoundPool(1, AudioManager.STREAM_MUSIC, 0);
		sound = soundPool.load(this, R.raw.morning, 1);
		className = this.getClass().getSimpleName();

	}

	@Override
	public int onStartCommand(Intent intent, int flags, int startId) {
		Log.i(className, "BeaconService Start");
		// Beacon Service Start
		//비콘 서비스 스타트.......
		//코드 구현...
        blueAdapter.startLeScan(mLeScanCallback);

		return START_NOT_STICKY;
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		Log.e(className, "BeaconService onDestroy");

		//비콘 서비스 종료
		//코드 구현....
        blueAdapter.stopLeScan(mLeScanCallback);


	}

	// LeScanCallback
	private BluetoothAdapter.LeScanCallback mLeScanCallback = new BluetoothAdapter.LeScanCallback() {

		private int tx;
		private int major;
		private int minor;
		private double distance;
		private double newDistance;

		public void onLeScan(BluetoothDevice device, int rssi, byte[] scanRecord) {

			remoteDevice = device;

			// if (device.toString().equals(addr)) {

			Log.e(className, "70 : onLeScan call -----");

			final BluetoothLeDevice deviceLe = new BluetoothLeDevice(device,
					rssi, scanRecord, System.currentTimeMillis());

			try {

				Log.e(className, "78 : Device " + deviceLe.getAddress());

				IBeaconManufacturerData iBeaconData = new IBeaconManufacturerData(
						deviceLe);
				tx = iBeaconData.getCalibratedTxPower();
				major = iBeaconData.getMajor();
				minor = iBeaconData.getMinor();
				distance = (float) rssi / (float) tx;
				newDistance = calculateAccuracy(tx, rssi);

				Log.e(className, "기존 거리 계산 : " + distance);

				// 수신한 Beacon 메세지를 파싱해서 관련작업 수행
				parseBeaconData(major, minor, newDistance);

			} catch (Exception e) {
				e.printStackTrace();
			}

			// }// end of if
		}// end of onLeScan

	};

	/*
	 * 1. 보완사항 : 값 보정 로직 2. isFrist
	 */
	private void parseBeaconData(int major, int minor, double distance) {

		//특정 거리(3미터 이내) 이내에 들어왔을때 major, minor 분석해서 실행하는 코드 구현하기
		//코드 구현 ~~~~~~~
		Log.e(className, "Beacon Data - Diatance: " + distance + ", Major/Minor : " + major + "/" + minor);
		if (distance < 0 || distance > 3.0) {
			return;
		}
		
		switch (major) {

		// 비콘 Major, Minor에 맞게 변경할 것 ---------------------
		
		case BEACON_MAJOR:
			switch (minor) {
			case BEACON_MINOR:
				if(isFrist){
					soundPool.play(sound, 1, 1, 0, 0, 1);
					isFrist = false;
					String phoneNum = CommonUtilities.getMyPhoneNum(this);
					Toast.makeText(this, phoneNum+" 번호 주인 지금 매장 왔어요...", Toast.LENGTH_SHORT).show();

					//서버에 매장에 들어온 고객정보 전달하기
					String url = CommonUtilities.MY_WEB_SERVER +"/O2OProject/main.do?action=enterStore&phoneNum=" + phoneNum;

					//해당 action으로 코드 구현하기...
					//화면에 매장에 들어온 고객의 정보를 이용하여 결과화면(주문내역) 표출하기
					//코드 구현 ----------------
					Log.e(className, "URL 정보 - " + url);
					Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
					intent.setFlags(FLAG_ACTIVITY_NEW_TASK);
					startActivity(intent);
					stopSelf();
				}
				break;
			case 11002:

				break;

			default:
				break;
			}
			break;
		// 서초동 가맹점
		case 12000:

			break;
		default:
			break;
		}
		if (major == 11000 && minor == 11001) {
			// if (distance < 1.0 && isFrist) {
			if (distance < 1.0) {
				
			}
		}
	}

	// IOS 거리 계산 공식
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

	@Override
	public IBinder onBind(Intent intent) {
		// TODO Auto-generated method stub
		return null;
	}

}
