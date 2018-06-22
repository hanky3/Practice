package com.jaen.o2o.jaenpay.nfc.record;

import android.net.Uri;

public class SmsRecord extends UriRecord {
	
	private String smsUri;
	
	public SmsRecord(String uri) {
		super(Uri.parse(uri));
		smsUri= uri;
	}

	public String getMessage() {
		
		int i = smsUri.indexOf("?body=");
		if (i > 0)
			;
		for (String str = smsUri.substring(i + 6);; str = null)
			return str;
	}

	public String getPhone() {
		
		int i = 0;
		if (smsUri.startsWith("sms:")) {
			i = smsUri.indexOf("?");
			if (i < 1)
				i = smsUri.length();
		}
		for (String str = smsUri.substring(4, i);; str = null)
			return str;
	}
}
