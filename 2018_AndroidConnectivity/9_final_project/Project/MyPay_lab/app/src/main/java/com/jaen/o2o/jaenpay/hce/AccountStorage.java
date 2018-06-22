package com.jaen.o2o.jaenpay.hce;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;

/**  
 * @version 1.0
 * @created 2014-11-25 
 * @description 저장된 카드 정보를 프래그먼트에 출력 
 * @reference http://developer.android.com/samples/CardEmulation/index.html
 * 
 * Utility class for persisting account numbers to disk.
 *
 * <p>The default SharedPreferences instance is used as the backing storage. Values are cached
 * in memory for performance.
 *
 * <p>This class is thread-safe.
 */
public class AccountStorage {
    private static final String PREF_ACCOUNT_NUMBER = "account_number";
    private static final String DEFAULT_ACCOUNT_NUMBER = "00000000";
    private static final String TAG = "AccountStorage";
    private static String sAccount = null;
    private static final Object sAccountLock = new Object();

    /**
     * 입력된 카드 정보를 SharedPreference에 저장하는 기능
     */
    public static void SetAccount(Context c, String s) {
        synchronized(sAccountLock) {
            Log.i(TAG, "Setting account number: " + s);
            SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(c);
            prefs.edit().putString(PREF_ACCOUNT_NUMBER, s).commit();
            sAccount = s;
        }
    }
    
    /**
     * 저장된 카드 정보를 SharedPreference에서 읽어오는 기능
     */
    public static String GetAccount(Context c) {
        synchronized (sAccountLock) {
            if (sAccount == null) {
                SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(c);
                String account = prefs.getString(PREF_ACCOUNT_NUMBER, DEFAULT_ACCOUNT_NUMBER);
                sAccount = account;
            }
            return sAccount;
        }
    }
}
