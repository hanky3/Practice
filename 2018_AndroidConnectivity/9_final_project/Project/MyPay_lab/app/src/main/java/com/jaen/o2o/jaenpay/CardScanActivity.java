package com.jaen.o2o.jaenpay;


import io.card.payment.CardIOActivity;
import io.card.payment.CreditCard;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;


/**
 * @version 1.0
 * @description 카드 스캔 등록
 * @reference https://github.com/card-io/card.io-Android-SDK
 */
public class CardScanActivity extends Activity {
	
	private static final int MY_SCAN_REQUEST_CODE = 100;
	private String resultStr;
	private String TAG = getClass().getSimpleName();
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		// TODO Auto-generated method stub
		super.onCreate(savedInstanceState);
		setContentView(R.layout.cardscan_layout);
	}
	
	//call-back 함수
	public void scanStart(View v){
		
		Intent scanIntent = new Intent(this, CardIOActivity.class);

		// customize these values to suit your needs.
		scanIntent.putExtra(CardIOActivity.EXTRA_REQUIRE_EXPIRY, true); // default:
																		// true
		scanIntent.putExtra(CardIOActivity.EXTRA_REQUIRE_CVV, false); // default:
																		// false
		scanIntent.putExtra(CardIOActivity.EXTRA_REQUIRE_POSTAL_CODE, false); // default:
																				// false

		// hides the manual entry button
		// if set, developers should provide their own manual entry mechanism in
		// the app
		scanIntent.putExtra(CardIOActivity.EXTRA_SUPPRESS_MANUAL_ENTRY, false); // default:
																				// false

		// MY_SCAN_REQUEST_CODE is arbitrary and is only used within this
		// activity.
		startActivityForResult(scanIntent, MY_SCAN_REQUEST_CODE);
		
	}
	
	/**
	 * 카드 회사 종류를 식별하는 함수
	 */
	public String checkType(String number) {
		String type = number;
		if (type.startsWith("51") || type.startsWith("52")
				|| type.startsWith("53") || type.startsWith("54")
				|| type.startsWith("55")) {
			type = "Mastercard";
		} else if (type.startsWith("4")) {
			type = "VISA";
		} else if (type.startsWith("5018") || type.startsWith("5020")
				|| type.startsWith("5038") || type.startsWith("5893")
				|| type.startsWith("6304") || type.startsWith("6759")
				|| type.startsWith("6761") || type.startsWith("6762")
				|| type.startsWith("6763")) {
			type = "Maestro";
		} else if (type.startsWith("6011") || type.startsWith("622")
				|| type.startsWith("644") || type.startsWith("645")
				|| type.startsWith("646") || type.startsWith("647")
				|| type.startsWith("648") || type.startsWith("649")
				|| type.startsWith("65")) {
			type = "DISCOVER";
		} else {
			type = "other";
		}
		return type;
	}

	/**
	 * ㄴ * 스캔된 카드 정보를 처리하는 함수
	 */
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);

		if (data != null && data.hasExtra(CardIOActivity.EXTRA_SCAN_RESULT)) {
			CreditCard scanResult = data
					.getParcelableExtra(CardIOActivity.EXTRA_SCAN_RESULT);
			String number = scanResult.cardNumber;
			String type = checkType(number);
			resultStr = scanResult.getFormattedCardNumber() + "\n";
			// Never log a raw card number. Avoid displaying it, but if
			// necessary use getFormattedCardNumber()
			// resultStr = scanResult.cardNumber;
			// resultStr += "카드 번호: " + scanResult.getRedactedCardNumber() +
			// "\n";
			// resultStr += "Formatted Card Number: " +
			// scanResult.getFormattedCardNumber() + "\n";
			// resultStr += "4 digits Card Number: " +
			// scanResult.getLastFourDigitsOfCardNumber() + "\n";
			// resultStr += "EX Card Number: " + scanResult.isExpiryValid() +
			// "\n";
			// Do something with the raw number, e.g.:
			// myService.setCardNumber( scanResult.cardNumber );

			if (scanResult.isExpiryValid()) {
				resultStr += scanResult.expiryMonth + "/"
						+ scanResult.expiryYear + "\n";
			}
			resultStr += type + "\n";

			/*
			 * if (scanResult.cvv != null) { // Never log or display a CVV
			 * resultStr += "CVV has " + scanResult.cvv.length() + " digits.\n";
			 * }
			 * 
			 * if (scanResult.postalCode != null) { resultStr += "Postal Code: "
			 * + scanResult.postalCode + "\n"; }
			 */

			Intent saveIntent = new Intent(this, SaveMyCardActivity.class);
			//sdj added
			saveIntent.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
			Log.e(TAG, resultStr);
			saveIntent.putExtra("cardInfo", resultStr);
			startActivity(saveIntent);
		} else {
			resultStr = "Scan was canceled.";
		}
		// resultTextView.setText(resultStr);

	}

}
