package com.memorykloud.Http;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URI;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

/**
 * Map<String, HttpPackage>: where String is a uuid to defined a particular job
 * whereas HttpPackage defines the URL, paramlist and the response
 * 
 * @author Jie Note: You can only execute an AsyncTask instance once, which
 *         means you can't recycle AsyncTask instance
 */
public class HttpRequestTask extends AsyncTask<Void, Void, Void> {
	private Map<String, HttpPackage> _package;
	private IHttpCallback<Void> _callback;
	private Context _context;
	private ProgressDialog _processdialog;
	private HTTPType _httpType;

	public enum HTTPType {
		GET, POST, POSTMULTIPART
	};

	public HttpRequestTask(Context context, IHttpCallback<Void> callback,
			HTTPType httpType) {
		this._callback = callback;
		this._context = context;
		this._httpType = httpType;
		this._package = new HashMap<String, HttpPackage>();
	}

	public void SetPackage(String uuid, HttpPackage pkg) {
		this._package.put(uuid, pkg);
	}

	public HttpPackage GetPackage(String uuid) {
		if (this._package.containsKey(uuid))
			return this._package.get(uuid);
		else
			return null;
	}

	public void RemovePackage(String uuid) {
		this._package.remove(uuid);
	}

	public void ClearPackage() {
		this._package.clear();
	}

	@Override
	protected void onPreExecute() {
		_processdialog = ProgressDialog.show(_context, "", "please wait...");
	}

	@Override
	protected Void doInBackground(Void... voidParam) {
		HttpClient httpClient = new DefaultHttpClient();

		for (Map.Entry<String, HttpPackage> entry : this._package.entrySet()) {
			// Only HttpPackage is needed here
			HttpPackage pkg = entry.getValue();
			String url = pkg.get_url();
			List<NameValuePair> params = pkg.get_params();
			MultipartEntity multiPartEntity = pkg.get_multipartEntity();

			try {
				HttpResponse response = null;

				switch (this._httpType) {
				case GET:
					// construct URL string by concatenating the params list
					if (params.size() > 0) {
						if (!url.endsWith("?"))
							url += "?";
						String paramString = URLEncodedUtils.format(params,
								"utf-8");
						url += paramString;
					}

					// run the get
					HttpGet httpget = new HttpGet();
					httpget.setURI(new URI(url));
					response = httpClient.execute(httpget);
					break;
				case POST:
					// run the post
					HttpPost httppost = new HttpPost(url);
					httppost.setEntity(new UrlEncodedFormEntity(params));
					response = httpClient.execute(httppost);
					break;
				case POSTMULTIPART:
					// run the post
					HttpPost httppostmultipart = new HttpPost(url);
					httppostmultipart.setEntity(multiPartEntity);
					response = httpClient.execute(httppostmultipart);
				}

				// process the returned value as a String
				BufferedReader reader = new BufferedReader(
						new InputStreamReader(
								response.getEntity().getContent(), "UTF-8"));
				String sResponse;
				StringBuilder s = new StringBuilder();
				while ((sResponse = reader.readLine()) != null) {
					s = s.append(sResponse);
				}
				sResponse = s.toString();

				// convert the string to JSONArray
				try {
					JSONArray jArray = new JSONArray(sResponse);
					pkg.set_response(jArray);
				} catch (Exception e) {
					// not a valid JSON object
					pkg.set_response(sResponse);
				}
			} catch (Exception e) {
				// handle exception here
				Log.e(e.getClass().getName(), e.getMessage());
			}
		}
		return null;
	}

	@Override
	protected void onPostExecute(Void result) {
		super.onPostExecute(result);
		_processdialog.dismiss();
		_callback.onHttpTaskComplete(result);
	}
}