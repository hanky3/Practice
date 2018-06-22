package edu.jaen.android.nfc.BlueBeam;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.nfc.NfcAdapter;
import android.nfc.NfcAdapter.CreateNdefMessageCallback;
import android.nfc.NfcAdapter.OnNdefPushCompleteCallback;
import android.nfc.NfcEvent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.Parcelable;
import android.provider.Settings;
import android.text.format.Time;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.nio.charset.Charset;


/*
 * setBeamPushUri를 이용하여 프로그램 구현
 * - Nfc와 Bluetooth가 자동으로 연동되어 실현되는 코드
 * - Bluetooth 기능이 활성화 되어 있지 않아도
 *   자동으로 활성화 시킨후 Data 전송 완료후 
 *   Bluetooth 모듈을 비활성화 시킨다.
 * 
 * 
 * */
public class MyBlueBeam extends Activity {

	NfcAdapter mNfcAdapter;
	TextView mInfoText;

	private static final int MESSAGE_SENT = 1;

	@Override
	public void onCreate(Bundle savedInstanceState) {

		super.onCreate(savedInstanceState);
		setContentView(R.layout.beam_layout);

		mInfoText = (TextView) findViewById(R.id.displayUriView);

		// Check for available NFC Adapter
		mNfcAdapter = NfcAdapter.getDefaultAdapter(this);

		if (mNfcAdapter == null) {
			mInfoText = (TextView) findViewById(R.id.textView);
			mInfoText.setText("NFC is not available on this device.");
			finish();
			return;
		}

		//전송할 파일을 선택함
		findViewById(R.id.selBut).setOnClickListener(
				new View.OnClickListener() {

					@Override
					public void onClick(View v) {

						Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
						intent.setType("image/*");
						startActivityForResult(intent, 1);

					}
				});
	}

	//선택된 파일을 이용하여 Uri 객체를 생성하고 setBeamPushUris를 이용하여 해당 Data를\
	//Bluetooth를 이용하여 전송한다. 
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);
		Uri uri = data.getData();
		mInfoText.setText("Sending: " + uri);
		// 이미지 : content://media/external/images/media/2898
		mNfcAdapter.setBeamPushUris(new Uri[] { uri }, this);
	}
}
