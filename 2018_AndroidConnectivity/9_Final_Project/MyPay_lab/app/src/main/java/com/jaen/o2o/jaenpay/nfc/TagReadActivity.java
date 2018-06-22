package com.jaen.o2o.jaenpay.nfc;

import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.jaen.o2o.jaenpay.BuildConfig;
import com.jaen.o2o.jaenpay.MainActivity;
import com.jaen.o2o.jaenpay.R;
import com.jaen.o2o.jaenpay.nfc.record.MimeRecord;
import com.jaen.o2o.jaenpay.nfc.record.ParsedNdefRecord;
import com.jaen.o2o.jaenpay.nfc.record.SmsRecord;
import com.jaen.o2o.jaenpay.nfc.record.TextRecord;
import com.jaen.o2o.jaenpay.nfc.record.UriRecord;

import android.app.Activity;
import android.app.PendingIntent;
import android.bluetooth.BluetoothAdapter;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.IntentFilter.MalformedMimeTypeException;
import android.media.AudioManager;
import android.net.Uri;
import android.net.wifi.WifiManager;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.nfc.tech.NfcF;
import android.os.Bundle;
import android.os.Parcelable;
import android.preference.PreferenceManager;
import android.provider.Browser;
import android.speech.tts.TextToSpeech;
import android.speech.tts.TextToSpeech.OnInitListener;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class TagReadActivity extends Activity {

	private TextView mTitle;
	private LinearLayout mTagContent;
	private LayoutInflater layoutInflater;
	private static final String TAG = "TagReadActivity";

	private NfcAdapter mAdapter;
	private PendingIntent mPendingIntent;
	private IntentFilter[] mFilters;
	private String[][] mTechLists;
	private TextView mText;
	private View tagShowView;

	private BluetoothAdapter blueAdapter;
	private WifiManager wifiMgr;
	private AudioManager audioMgr;

	private TextToSpeech tts;

	// private boolean executeProgram = true;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		//setContentView(R.layout.read_tag);

		System.out.println("72--------");
		layoutInflater = ((LayoutInflater) getSystemService("layout_inflater"));

		mAdapter = NfcAdapter.getDefaultAdapter(this);
		blueAdapter = BluetoothAdapter.getDefaultAdapter();
		wifiMgr = (WifiManager) getSystemService(WIFI_SERVICE);
		audioMgr = (AudioManager) getSystemService(AUDIO_SERVICE);

		//ts = new TextToSpeech(this, this);

		Intent passedIntent = getIntent();

		System.out.println("84 : passedIntent=" + passedIntent);

		if (passedIntent != null) {
			System.out.println("87--------");
			String action = passedIntent.getAction();
			System.out.println("83 : action=" + action);
			if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(action)
					|| NfcAdapter.ACTION_TECH_DISCOVERED.equals(action)
					|| NfcAdapter.ACTION_TAG_DISCOVERED.equals(action)) {
				resolveIntent(passedIntent);
			}
		}

	}

	private void resolveIntent(Intent intent) {
		System.out.println("91 : resolveIntent called...intent.getAction="
				+ intent.getAction());
		// Parse the intent
		String action = intent.getAction();
		if (NfcAdapter.ACTION_NDEF_DISCOVERED.equals(action)
				|| NfcAdapter.ACTION_TECH_DISCOVERED.equals(action)
				|| NfcAdapter.ACTION_TAG_DISCOVERED.equals(action)) {
			// When a tag is discovered we send it to the service to be save. We
			// include a PendingIntent for the service to call back onto. This
			// will cause this activity to be restarted with onNewIntent(). At
			// that time we read it from the database and view it.
			Parcelable[] rawMsgs = intent
					.getParcelableArrayExtra(NfcAdapter.EXTRA_NDEF_MESSAGES);
			NdefMessage[] msgs;
			if (rawMsgs != null) {
				msgs = new NdefMessage[rawMsgs.length];
				for (int i = 0; i < rawMsgs.length; i++) {
					msgs[i] = (NdefMessage) rawMsgs[i];
				}
			} else {
				// Unknown tag type
				byte[] empty = new byte[] {};
				NdefRecord record = new NdefRecord(NdefRecord.TNF_UNKNOWN,
						empty, empty, empty);
				NdefMessage msg = new NdefMessage(new NdefRecord[] { record });
				msgs = new NdefMessage[] { msg };
			}

			/*
			 * executeProgram의 설정값이 true 이면 해당 프로그램을 실행하고 flase이면 화면에 해당 record에
			 * 담긴 값을 표출한다.
			 */

			doAction(msgs);

		} else {
			Log.e(TAG, "Unknown intent " + intent);
			// NfcInfoUtil.getInstance(this).showToast("Unknown Type 입니다...");
			finish();
			return;
		}
	}

	private void buildTagViews(NdefMessage[] msgs) {

		if (msgs == null || msgs.length == 0) {
			return;
		}

		// View tagView = layoutInflator.inflate(R.layout.tag_viewer, null);
		//
		// mTagContent = (LinearLayout) tagView.findViewById(R.id.list);
		// mTitle = (TextView) tagView.findViewById(R.id.title);

		// LayoutInflater inflater = LayoutInflater.from(this);
		LinearLayout content = mTagContent;
		// Clear out any old views in the content area, for example if you scan
		// two tags in a row.
		content.removeAllViews();
		// Parse the first message in the list
		// Build views for all of the sub records
		List<ParsedNdefRecord> records = NdefMessageParser.parse(msgs[0]);
		final int size = records.size();
		for (int i = 0; i < size; i++) {
			ParsedNdefRecord record = records.get(i);
			// content.addView(record.getView(this, inflater, content, i));
			// inflater.inflate(R.layout.tag_divider, content, true);
			content.addView(record.getView(this, layoutInflater, content, i));
			layoutInflater.inflate(R.layout.tag_divider, content, true);
		}

		setContentView(tagShowView);

	}

	private void doAction(NdefMessage[] msgs) {

		List<ParsedNdefRecord> records = NdefMessageParser.parse(msgs[0]);

		final int size = records.size();
		System.out.println("doAction parse data size : " + size);

		for (int i = 0; i < size; i++) {

			ParsedNdefRecord record = records.get(i);

			if (record instanceof UriRecord) {

				//Record 분석해서 코드 구현하기.... sms, url, tel 등






			} else if (record instanceof TextRecord) {

				//buildTagViews(msgs);




			} else if (record instanceof MimeRecord) {

				//ShopMode에 맞게 실행하기...
				//Bluetooth 활성화, 진동모드 활성화....
				//코드 구현...
				String data = ((MimeRecord) record).getMimeData();
				String[] mode = data.split("/");
				if (mode.length < 2 || !mode[0].equals("jaMode")) {
					if (mode.length >= 1)
						Log.e("INFO", "Invalid Tag Info - " + mode[0]);
					return;
				}

				Pattern p = Pattern.compile("^([a-zA-Z]+)/B:([0-9]+)&R:([0-9]+)");
				Matcher m = p.matcher(data);
				if (m.find()) {
					String msg = "Matched - Prefix(" + m.group(1) + "), B(" + m.group(2) + "), R(" + m.group(3) + ")";
					Log.e("INFO", msg);

					String bluetoothMode = m.group(2);
					String pagerMode = m.group(3);

					changeMode(new String[]{"B", bluetoothMode});
					changeMode(new String[]{"R", pagerMode});
					Toast.makeText(this, msg, Toast.LENGTH_SHORT).show();
				}
				startActivity(new Intent(this, MainActivity.class));
			} else {

			}

		}

	}

	private void doCall(String uri) {
		Intent localIntent2 = new Intent(Intent.ACTION_CALL, Uri.parse(uri));
		//직전 전화거는 기능 수행~~
		//startActivity(localIntent2);
	}

	private void doSms(String uri) {
		SmsRecord smsR = new SmsRecord(uri);
		String phone = smsR.getPhone();
		String message = smsR.getMessage();
		Intent localIntent3 = new Intent(Intent.ACTION_SENDTO, Uri.parse("sms:"
				+ phone));
		if (message != null)
			localIntent3.putExtra("sms_body", message);
		startActivity(localIntent3);

		// 곧바로 SMS를 보내는 기능
		// SmsManager smsMgr = SmsManager.getDefault();
		// smsMgr.sendTextMessage(phone, null, message, null, null);
	}

	private void doUrl(String uri) {
		//특정 사이트로 이동하는 코드 구현하기 ~~



	}

	public void doShopMode(String mode) {

		//쇼핑 모드 코드 구현하기.....
		//://B1&R1








		Toast.makeText(this, "쇼핑모드로 변경되었습니다..", Toast.LENGTH_SHORT).show();
		startMain();
		finish();

	}

	private void changeMode(String[] modeArr) {

		Log.e("info", "changeMode start ...");

		// tts.speak("Hi Dong Jin your phone is Shopping mode good luck",
		// TextToSpeech.QUEUE_FLUSH, null);

		if (modeArr[0].equalsIgnoreCase("B")
				&& modeArr[1].equalsIgnoreCase("1")) {
			blueAdapter.enable();
		}
		if (modeArr[0].equalsIgnoreCase("R")
				&& modeArr[1].equalsIgnoreCase("1")) {
			audioMgr.setRingerMode(AudioManager.RINGER_MODE_VIBRATE);
		}
		if (modeArr[0].equalsIgnoreCase("W")
				&& modeArr[1].equalsIgnoreCase("1")) {
			wifiMgr.setWifiEnabled(true);
		}
		Log.e("info", "changeMode end ...");

	}

	public void startMain() {

		startActivity(new Intent(this, MainActivity.class));

	}

	@Override
	public void onNewIntent(Intent intent) {
		Log.i("sdj", "159 : onNewIntent() called..");
		System.out.println("159 : onNewIntent() called..");
		setIntent(intent);
		resolveIntent(intent);
	}

	@Override
	public void setTitle(CharSequence title) {
		mTitle.setText(title);
	}

	@Override
	protected void onResume() {
		// TODO Auto-generated method stub
		super.onResume();
	}

	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		// if (mAdapter != null) {
		// mAdapter.disableForegroundDispatch(this);
		// }
	}



	public void onDestroy() {
		if (tts != null) {

			tts.stop();
			tts.shutdown();
		}
		super.onDestroy();
	}

}
