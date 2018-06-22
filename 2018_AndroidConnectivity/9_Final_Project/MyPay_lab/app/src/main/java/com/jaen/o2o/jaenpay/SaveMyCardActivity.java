package com.jaen.o2o.jaenpay;

import com.jaen.o2o.jaenpay.hce.AccountStorage;
import com.jaen.o2o.jaenpay.hce.HCEMainActivity;

import io.card.payment.CardIOActivity;
import io.card.payment.CreditCard;
import android.app.Activity;
import android.app.Fragment;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

/**
 * @version 1.0
 * @created 2014-12-03
 * @description HCE 카드 생성을 위해 추가 정보를 입력 받고 카드 정보를 저장
 */
public class SaveMyCardActivity extends FragmentActivity {
	private TextView resultTextView;
	private Button HCEButton;
	private String resultStr;
	private String cvcRedacted;
	private String cvc;
	private EditText cvc_field;
	private EditText first_name_field;
	private EditText last_name_field;
	private String first_name;
	private String last_name;
	private String TAG = getClass().getSimpleName();

	SharedPreferences mPref;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.cardinfo);
		HCEButton = (Button) findViewById(R.id.HCEButton);
		resultTextView = (TextView) findViewById(R.id.resultTextView);

		Intent saveIntent = getIntent();
		resultStr = saveIntent.getStringExtra("cardInfo");
		Log.e(TAG, "onCreate 59 cardInfo : " + resultStr);
		resultTextView.setText(resultStr);

		cvc_field = (EditText) findViewById(R.id.cvc_field);
		first_name_field = (EditText) findViewById(R.id.first_name_field);
		last_name_field = (EditText) findViewById(R.id.last_name_field);
	}

	private boolean validate() {
		if (first_name_field.getText().toString().trim().equals("")) {
			Toast.makeText(getBaseContext(), "First Name을 입력해주세요!",
					Toast.LENGTH_SHORT).show();
			return false;
		} else if (last_name_field.getText().toString().trim().equals("")) {
			Toast.makeText(getBaseContext(), "Last Name을 입력해주세요!",
					Toast.LENGTH_SHORT).show();
			return false;
		} else if (cvc_field.getText().toString().trim().equals("")) {
			Toast.makeText(getBaseContext(), "CVC코드를 입력해주세요!",
					Toast.LENGTH_SHORT).show();
			return false;
		} else if (cvc_field.getText().toString().trim().length() < 3) {
			Toast.makeText(getBaseContext(), "CVC코드 세자리를 입력해주세요!",
					Toast.LENGTH_SHORT).show();
			return false;
		} else
			return true;
	}

	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
		switch (keyCode) {
		case KeyEvent.KEYCODE_BACK:
			finish();
			return false;
		default:
			return false;
		}
	}

	/**
	 * HCE 카드 생성을 위해 영문 이름(성), cvc 코드 등을 입력 받아서 다음 액티비티로 전달
	 */
	public void onHCEGenerate(View v) {

		if (validate()) {
			cvc = cvc_field.getText().toString().trim();
			first_name = first_name_field.getText().toString().toUpperCase()
					.trim();
			last_name = last_name_field.getText().toString().toUpperCase()
					.trim();

			SharedPreferences prefs = PreferenceManager
					.getDefaultSharedPreferences(this);
			String regId = prefs.getString("regId", "noregId");
			String u_num = prefs.getString("u_num", "0");
			System.out.println(" 카드 만들 때 regId" + regId);

			resultStr += first_name + "\t";
			resultStr += last_name + "\n";
			resultStr += cvc + "\n";
			resultStr += regId + "\n";
			resultStr += u_num;

			System.out.println("save " + resultStr);

			mPref = PreferenceManager
					.getDefaultSharedPreferences(getApplicationContext());
			SharedPreferences.Editor editor = mPref.edit();
			editor.putString("account_number", resultStr);
			editor.commit();

			AccountStorage.SetAccount(getApplicationContext(), resultStr);
			Intent i = new Intent(this, HCEMainActivity.class);
			i.putExtra("account", resultStr);
			//i.addFlags(i.FLAG_ACTIVITY_NO_HISTORY);
			startActivity(i);
		}
	}

}
