/*
 * Copyright (C) 2010 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.jaen.o2o.jaenpay.nfc.record;

import android.app.Activity;
import android.net.Uri;
import android.nfc.NdefMessage;
import android.nfc.NdefRecord;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.common.base.Preconditions;
import com.google.common.collect.BiMap;
import com.google.common.collect.ImmutableBiMap;
import com.google.common.primitives.Bytes;



import com.jaen.o2o.jaenpay.R;

import java.nio.charset.Charset;
import java.util.Arrays;

public class MimeRecord implements ParsedNdefRecord {

	private static final String TAG = "MimeRecord";
	public static final String RECORD_TYPE = "MimeRecord";
	private final String mimeData;

	public MimeRecord(String data) {
		mimeData = data;
	}

	public String getMimeData() {
		return mimeData;
	}

	public View getView(Activity activity, LayoutInflater inflater,
			ViewGroup parent, int offset) {
		TextView text = (TextView) inflater.inflate(R.layout.tag_text, parent,
				false);
		text.setText(getMimeData());
		return text;
	}

	public static MimeRecord parse(NdefRecord record) {
		short tnf = record.getTnf();
		if (tnf == NdefRecord.TNF_MIME_MEDIA) {
			String data = new String(record.getPayload());
			return new MimeRecord(data);
		}
		throw new IllegalArgumentException("Unknown TNF " + tnf);
	}

	public static boolean isMime(NdefRecord record) {
		try {
			parse(record);
			return true;
		} catch (IllegalArgumentException e) {
			return false;
		}
	}

	private static final byte[] EMPTY = new byte[0];
}
