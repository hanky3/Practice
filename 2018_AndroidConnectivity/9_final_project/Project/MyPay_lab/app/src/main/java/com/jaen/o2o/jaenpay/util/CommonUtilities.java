package com.jaen.o2o.jaenpay.util;



import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.telephony.TelephonyManager;

/**
 * @version 1.0
 * @description GCM에 활용되는 상수 및 기능 정의
 * @reference http://developer.android.com/google/gcm/index.html
 */
public final class CommonUtilities {

	public static final int MAJOR_CODE = 36757;
	public static final int MINOR_CODE = 15036;
	/**
	 * Base URL of the Demo Server (such as http://my_host:8080/gcm-demo)
	 */
	public static final String SERVER_URL = "https://70.12.109.173:5555";
	// SDJ
	//public static final String MY_WEB_SERVER = "http://192.168.168.102";
	// 192.168.42.132
	 public static final String MY_WEB_SERVER = "http://192.168.0.159";
	/**
	 * Google API project id registered to use GCM.
	 */
	static final String SENDER_ID = "138649741148";

	/**
	 * Tag used on log messages.
	 */
	static final String TAG = "GCMDemo";

	/**
	 * Intent used to display a message in the screen.
	 */
	static final String DISPLAY_MESSAGE_ACTION = "com.google.android.gcm.demo.app.DISPLAY_MESSAGE";

	/**
	 * Intent's extra that contains the message to be displayed.
	 */
	static final String EXTRA_MESSAGE = "message";

	/**
	 * Notifies UI to display a message.
	 * <p>
	 * This method is defined in the common helper because it's used both by the
	 * UI and the background service.
	 *
	 * @param context
	 *            application's context.
	 * @param message
	 *            message to be displayed.
	 */
	static void displayMessage(Context context, String message) {
		Intent intent = new Intent(DISPLAY_MESSAGE_ACTION);
		intent.putExtra(EXTRA_MESSAGE, message);
		context.sendBroadcast(intent);
	}

	public static String getMyPhoneNum(Context ctx) {
		TelephonyManager telManager = (TelephonyManager) ctx
				.getSystemService(Context.TELEPHONY_SERVICE);
		//String phoneNum = telManager.getLine1Number().substring(1);
		String phoneNum = "01090070397";
		return phoneNum;
	}

	public static void showDialog(Context ctx, String title, String msg) {
//		AlertDialog.Builder dialog = new AlertDialog.Builder(ctx);
//		dialog.setIcon(android.R.drawable.ic_dialog_info).setTitle(msg)
//				.setMessage(msg).setPositiveButton("확인", null);
//		dialog.show();
		
		AlertDialog.Builder dialog = new AlertDialog.Builder(ctx);
		dialog.setIcon(android.R.drawable.ic_dialog_info).setTitle("알림")
				.setMessage("알립니다").setPositiveButton("확인", null);
		dialog.show();
	}

}
