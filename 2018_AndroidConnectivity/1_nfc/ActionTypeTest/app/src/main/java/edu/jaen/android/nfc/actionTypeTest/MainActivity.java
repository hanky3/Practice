package edu.jaen.android.nfc.actionTypeTest;

import java.io.File;
import java.io.IOException;

import android.media.AudioManager;
import android.net.Uri;
import android.net.wifi.WifiManager;
import android.nfc.tech.Ndef;
import android.os.Bundle;
import android.os.Vibrator;
import android.provider.MediaStore.Audio;
import android.app.Activity;
import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Toast;

public class MainActivity extends Activity implements OnClickListener {

	public static final int PICK_IMAGE = 1;
	public static final int PICK_AUDIO = 2;
	public static final int PICK_VIDEO = 3;
	
	private BluetoothAdapter blueAdapter;
	private WifiManager wifiMgr;
	private AudioManager audioMgr;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		findViewById(R.id.blueOnBut).setOnClickListener(this);
		findViewById(R.id.blueOffBut).setOnClickListener(this);
		findViewById(R.id.wifiOnBut).setOnClickListener(this);
		findViewById(R.id.wifiOffBut).setOnClickListener(this);
		findViewById(R.id.vibrBut).setOnClickListener(this);
		findViewById(R.id.getFileBut).setOnClickListener(this);
		findViewById(R.id.doAllBut).setOnClickListener(this);
		findViewById(R.id.goMarketBut).setOnClickListener(this);

		blueAdapter = BluetoothAdapter.getDefaultAdapter();
		wifiMgr = (WifiManager) getSystemService(WIFI_SERVICE);
		audioMgr = (AudioManager) getSystemService(AUDIO_SERVICE);
		
		
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public void onClick(View v) {
		switch (v.getId()) {
		case R.id.blueOnBut:
			blueAdapter.enable();
			break;
		case R.id.blueOffBut:
			blueAdapter.disable();
			break;
		case R.id.wifiOnBut:
			wifiMgr.setWifiEnabled(true);
			break;
		case R.id.wifiOffBut:
			wifiMgr.setWifiEnabled(false);
			break;
		case R.id.vibrBut:
			Toast.makeText(this,"111 : "+audioMgr.getRingerMode() ,0).show();
			if(audioMgr.getRingerMode() == AudioManager.RINGER_MODE_VIBRATE){
				audioMgr.setRingerMode(AudioManager.RINGER_MODE_NORMAL);
				Toast.makeText(this, convertMode(audioMgr.getRingerMode()), Toast.LENGTH_SHORT).show();
				
			}else if(audioMgr.getRingerMode() == AudioManager.RINGER_MODE_NORMAL){
				audioMgr.setRingerMode(AudioManager.RINGER_MODE_SILENT);
				Toast.makeText(this, convertMode(audioMgr.getRingerMode()), Toast.LENGTH_SHORT).show();
				
			}else if(audioMgr.getRingerMode() == AudioManager.RINGER_MODE_SILENT){
				audioMgr.setRingerMode(AudioManager.RINGER_MODE_VIBRATE);
				Toast.makeText(this, convertMode(audioMgr.getRingerMode()), Toast.LENGTH_SHORT).show();
				
			}
			break;
		case R.id.getFileBut:
			Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
			//image
//			intent.setType("image/*");
//			startActivityForResult(intent, PICK_IMAGE);
//			intent.setType("video/*");
//			startActivityForResult(intent, PICK_VIDEO);
			intent.setType("audio/*");
			startActivityForResult(intent, PICK_AUDIO);
			break;
		case R.id.doAllBut:
			blueAdapter.enable();
			wifiMgr.setWifiEnabled(true);
			audioMgr.setRingerMode(AudioManager.RINGER_MODE_VIBRATE);
			break;
		case R.id.goMarketBut:
			Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse("market://details?id="));
			startActivity(i);
			break;
		default:
			break;
		}

	}
	
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		// TODO Auto-generated method stub
		super.onActivityResult(requestCode, resultCode, data);
		switch (requestCode) {
		case PICK_IMAGE :
			String imagePath = data.getData().toString();
			Toast.makeText(this, imagePath, Toast.LENGTH_SHORT).show();
			break;
		case PICK_AUDIO :
			String audioPath = data.getData().toString();
			Toast.makeText(this, audioPath, Toast.LENGTH_SHORT).show();
			break;
		default:
			break;
		}
	}

	private void playAudio(String path) {
		Intent localIntent1 = new Intent("android.intent.action.VIEW");
		localIntent1.setDataAndType(Uri.parse(path), "video/*");
		startActivity(localIntent1);
	}

	private void playVideo(String path) {
		Intent localIntent1 = new Intent("android.intent.action.VIEW");
		localIntent1.setDataAndType(Uri.parse(path), "video/*");
		startActivity(localIntent1);
	}

	private void playImage(String path) {
		Intent localIntent2 = new Intent("android.intent.action.VIEW");
		localIntent2.setDataAndType(Uri.fromFile(new File(path)), "image/*");
		startActivity(localIntent2);

	}

	private String convertMode(int mode) {
		String result = "";
		switch (mode) {
		case AudioManager.RINGER_MODE_SILENT:
			result = "Silent 모드";
			break;
		case AudioManager.RINGER_MODE_VIBRATE:
			result = "진동 모드";
			break;
		case AudioManager.RINGER_MODE_NORMAL:
			result = "벨 모드";
			break;

		default:
			result = "나두 몰라";
			break;
		}

		return result;
	}

}
