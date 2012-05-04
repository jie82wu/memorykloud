package com.memorykloud.Http;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;

public class HttpPackage {
	private String _url;
	private List<NameValuePair> _nameValuePairs;
	private MultipartEntity _multipartEntity;
	private Object _response;

	public HttpPackage(String url) {
		this._url = url;
	}

	public HttpPackage(String url, List<NameValuePair> params) {
		this._url = url;
		this._nameValuePairs = params;
	}
	
	public HttpPackage(String url, MultipartEntity multipart) {
		this._url = url;
		this._multipartEntity = multipart;
	}
	
	public String get_url() {
		return _url;
	}

	public void set_url(String _url) {
		this._url = _url;
	}

	public List<NameValuePair> get_params() {
		if (this._nameValuePairs == null)
			this._nameValuePairs = new ArrayList<NameValuePair>();
		return _nameValuePairs;
	}

	public void set_params(List<NameValuePair> _params) {
		this._nameValuePairs = _params;
	}

	public Object get_response() {
		return _response;
	}

	public void set_response(Object _response) {
		this._response = _response;
	}

	public MultipartEntity get_multipartEntity() {
		if (this._multipartEntity==null){
			this._multipartEntity = new MultipartEntity(
					HttpMultipartMode.BROWSER_COMPATIBLE);
		}			
		return _multipartEntity;
	}

	public void set_multipartEntity(MultipartEntity _multipartEntity) {
		this._multipartEntity = _multipartEntity;
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		// TODO Auto-generated method stub
		return super.clone();
	}

	@Override
	public boolean equals(Object o) {
		// TODO Auto-generated method stub
		return super.equals(o);
	}

	@Override
	protected void finalize() throws Throwable {
		// TODO Auto-generated method stub
		super.finalize();
	}

	@Override
	public int hashCode() {
		// TODO Auto-generated method stub
		return super.hashCode();
	}

	@Override
	public String toString() {
		// TODO Auto-generated method stub
		return super.toString();
	}
}