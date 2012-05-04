package com.memorykloud.Http;

public interface IHttpCallback<T> {
	public void onHttpTaskComplete(T result);
}