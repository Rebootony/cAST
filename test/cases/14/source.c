int main()
{
  int a = 0;
  while(1) {
    func();
  }

  do {
    func();
    a += 1;
  } while(0);
  
  switch(a)
  {
    case 0:
      func();
      a += 1;
      break;
    case 1:
      func();
      goto byebye;
      break;
    default:
      break;
  }

byebye:
  printf("See ya!");
  return 0;
}

int func()
{
  return 0;
}
